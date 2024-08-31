---
title: "Comment j'ai enrichi des métriques Prometheus"
summary: Les métriques de l'exportateur VMWare n'avaient pas toutes les informations que nous voulions. Voici comment je les ai enrichies.
cover: "2022-05-06.jpg"
cover_alt: "couverture de l'article sur l'enrichissement des métriques prometheus"
publish_date: 2022-05-05T09:30:00Z
update_date: 2022-05-05T09:30:00Z
tags: [prometheus, python, pandas, dataframe, vmware exporter, fastapi]
---

## Contexte

Dans ma mission actuelle, afin de mettre en place une fédération de métriques, nous devons collecter des métriques VMware.

Nous avons donc utilisé le [vmware_exporter](https://github.com/pryorda/vmware_exporter) de [Daniel Pryor](https://github.com/pryorda), et pour ne pas le modifier, j'ai écrit une petite interface avec fastapi.

Les métriques sont récupérées par fastapi, analysées, enrichies, resérialisées, et récoltées par prometheus.

Les noms des métriques doivent être mappés, car ils sont unifiés avec les métriques d'openstack et d'IBM cloud.

La table de mappage est celle ci-dessous :

<pre>
MAPPING_METRICS_NAME = {
    "vmware_vm_power_state" : "power_state"
    "vmware_vm_cpu_usage_average"': "cpu_usage_percentage
    "vmware_vm_mem_consumed_average": "memory_used"
    "vmware_vm_memory_max": "memory_total"
    "vmware_vm_mem_usage_average": "memory_usage_percentage",
    "vmware_vm_num_cpu": "vcpus"
}</pre>

## Étape 1 : Analyse des métriques de vmware_exporter

L'exportateur est appelé depuis une fonction nommée request_exporter().

La sortie de l'exportateur est un grand fichier str qui doit être analysé pour être traité.

J'ai utilisé prometheus_client.parser pour cela.

<pre>
from prometheus_client.parser import text_string_to_metric_families

data_from_exporter = request_exporter(target)
metric_families = text_string_to_metric_families(data_from_exporter)
</pre>

La variable metric_families est un objet à plusieurs niveaux contenant des métriques regroupées par nom de métrique.

Elle peut être représentée comme un dict, où la clé est le metric_name et la valeur est une liste contenant toutes les métriques sous forme de tuples.

Exemple :
<pre>
{
    "vmware_vm_power_state": [
        ("vmware_vm_power_state", {"vm_name": "vm1", "label2": "value2"}, 1),
        ("vmware_vm_power_state", {"vm_name": "vm2", "label2": "value2"}, 0),
    ]
}
</pre>

J'ai donc fait un petit algorithme pour aplatir l'objet en une liste de dicts :

<pre>
processed_exporter_data = []

for family in data_from exporter:
    if family.name not in MAPPING_METRICS_NAME:
        continue
    for sample in family.samples:
        row dict = {}
        row dict["__name__"] = sample
        for key, value in sample.items():
            row dict[key] = value
        row_dict["value"] = sample
        processed exporter_data.append(row_dict)
</pre>

J'aurai alors une liste de dicts, à partir de laquelle un dataframe peut être créé.

<pre>
[
    {"__name__": "vmware_vm_power_state", "vm_name": "vm1", "value": 1},
    {"__name__": "vmware_vm_power_state", "vm_name": "vm2", "value": 0},
]
</pre>

Maintenant, jouons avec les dataframes...

## Étape 2 : Jouer avec les dataframes

Tout d'abord, je crée le dataframe :

<pre>
import pandas

metrics_df = pandas.DataFrame(processed_exporter_data)
</pre>

Ensuite, je supprime les étiquettes inutiles :

<pre>
metrics_df.drop(
    colums=[
        "host_name",
        "ds_name",
        "dc_name",
        "cluster_name",
    ],
    axis=1,
    inplace=True,
)
</pre>

De cette façon, j'utilise le dataframe pour supprimer les 4 colonnes. <code>inplace=True</code> est utilisé pour écraser le dataframe existant et ne pas en créer un nouveau.

Ensuite, je dois fusionner les données de métriques avec les données de deux autres sources de données internes (une pour le référentiel des hôtes/vm, une pour les lignes métier).

Celles-ci sont également représentées sous forme de dataframes.

<pre>
businesslines_referential_df = referential_df.merge(
    businesslines_df, how="left", left_on="ecosystem", right_index=True
)
</pre>

Cette fusion enrichira le dataframe référentiel avec les données des lignes métier, de droite à gauche, selon le nom de l'écosystème et utilisera l'index du dataframe de droite comme clé de jointure.

Maintenant, il est temps de fusionner ce dataframe avec le dataframe des métriques.

<pre>
metrics_df = metrics_df.merge(
    businesslines_referential_df, how="inner", left_on="vm_name", right_index=True
)
</pre>

Cette fusion est faite avec la méthode inner, ainsi nous ne gardons que les colonnes communes, selon vm_name.

Maintenant, je remplace le nom de métrique original par le mappage dont nous avons parlé plus tôt :

<pre>
metrics_df.replace({"__name_": MAPPING_METRICS_NAME}, inplace=True)
</pre>

Maintenant "vmware_vm_power_state" est mappé à "power_state".

Le résultat est similaire à ceci :

<table width="100%" border="1px">
    <tr>
        <th>__name__</th>
        <th>vm_name</th>
        <th>ecosystem</th>
        <th>business_line</th>
        <th>value</th>
    </tr>
    <tr>
        <td>power_state</td>
        <td>vm1</td>
        <td>TESTECO</td>
        <td>BL1</td>
        <td>1</td>
    </tr>
</table>

Maintenant, pour être récoltées par prometheus, ces données doivent être resérialisées.

## Étape 3 : Comment ai-je resérialisé les données ?

Les chaînes de métriques Prometheus sont assez simples :

<pre>
metric_name{label1="value1", label2="value2"} 0
</pre>

En utilisant une compréhension de liste, j'itère sur le dataframe pour imprimer une chaîne contenant au début le metric_name et à la fin la metric_value.

<pre>
return "\n".join(
    [
        f"{row['__name__']}{generate_dict_label(row)} {row['value']}"
        for index, row in metrics df.iterrows()
    ]
)
</pre>

La partie délicate est de générer les étiquettes, car nous ne pouvons pas modifier la sortie d'un dict en python.

Un dict en python ressemble à <code>{"key": "value"}</code>, nous devons générer une chaîne qui ressemble à <code>{label="value"}</code>

J'ai donc écrit une petite fonction qui génère cette chaîne.

<pre>
def generate_dict_label(row):

    labels = set(row.index) - {"__name__", "value"}

    return (
        "{"
        + ",".join(
            [
                f'{key}="{value}"'
                for key, value in row.items()
                if key in labels
            ]
        )
        + "}"
    )
</pre>

Finalement, les données sérialisées ressemblent à :

<pre>
power_state{vm_name="vm1", ecosystem="TESTECO", business_line="BL1"} 1
</pre>

Maintenant, les métriques sont récoltées par prometheus en appelant un petit module fait avec fastapi, qui analysera, enrichira et resérialisera les données provenant d'un exportateur prometheus vmware.

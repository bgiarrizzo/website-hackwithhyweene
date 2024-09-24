---
category_id: 1
category: Bases

module_id: 1
module: Git
module_logo: logo.png
module_description: "Git est un système de contrôle de version distribué gratuit et open source conçu pour gérer tout, des petits aux très grands projets avec rapidité et efficacité."

id: 1
title: Intro
summary: "Résumé"

publish_date: 2024-09-09T09:30:00Z
update_date: 2024-09-09T09:30:00Z
---

## A Propos de la gestion des versions

Pourquoi se soucier de la gestion des versions ?

Un VCS (Version Control System) est un système qui enregistre les modifications apportées à un fichier ou à un ensemble de fichiers au fil du temps afin que vous puissiez revenir a un état antérieur d'un fichier si besoin.

En tant que développeur, utiliser un VCS est très sage. Cela permet de garder toutes les versions d'un fichier, à tout moment. Un VCS permet également de travailler en équipe sur un projet ou une fonctionnalité, de voir qui a introduit quelle ligne, à quel endroit, à quel moment.

Utiliser un VCS permet de rester serein, de ne pas avoir peur de casser quelque chose, de pouvoir revenir en arrière si besoin.

### Faire des copies

La première méthode, également la plus simple et la moins fiable, est de copier les fichiers manuellement.

Pour résumer, vous travaillez dans le dossier de travail "code" et vous copiez manuellement le dossier de travail dans un autre dossier pour conserver une version de sauvegarde (par exemple code-dateDuJour ou code-fonctionnaliteA)

Cela fonctionne, mais c'est très limité et peu fiable.

On a vite fait de se tromper de dossier, d'écraser le mauvais fichier, etc.

### Les VCS locaux

Ces VCS utilisent une base de données locale pour stocker les modifications apportées aux fichiers.

RCS (Revision Control System) est un exemple de VCS local.

Ce type de VCS stocke la copie complète d'un fichier, et ne garde que les changements réalisés entre les versions.

Exemple :

Nous avons un fichier `fichier.txt` de 150 lignes.

Si je modifie 10 lignes, le VCS local va stocker mon nouveau fichier de 160 lignes, et un journal des modifications, contenant les 10 lignes modifiées.

### Les VCS centralisés

Dans le cas d'un VCS centralisé, un serveur central regroupe toutes les sources et les versions de chaque fichier.

Les développeurs travaillent sur une copie locale des fichiers, et envoient leurs modifications au serveur central.

Exemple :

- SVN (Subversion)
- CVS (Concurrent Versions System)

### Les VCS distribués

## Histoire de Git

## Concepts Clés

### Repository

### Commit

### Branch

### Remote

## Les bases de Git

## La CLI

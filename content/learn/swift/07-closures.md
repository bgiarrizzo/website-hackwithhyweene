---
id: 7
title: Closures
summary: "Les closures sont des blocs de code qui peuvent être stockés et passés autour de votre code, puis exécutés ultérieurement. Elles sont similaires aux blocs en Objective-C et aux lambdas en d'autres langages de programmation."
tags: swift, swift playground, xcode, closures

prism_needed: true

publish_date: 2024-11-21T22:45:00Z
update_date: 2024-11-21T22:45:00Z
---

Une closure est un bloc de code qui peut être stocké dans une variable, et executé à l'appel de cette variable.

## Closure basique

Mettons que je veux créer une closure qui affiche "Hello, world!".

```swift
let sayHello = {
    print("Hello, world!")
}
```

Ceci créé une fonction sans nom, mais qui peut être appelée en utilisant la variable `sayHello`.

```swift
sayHello() // Affiche "Hello, world!"
```

## Closure avec paramètres

Les closures peuvent accepter des paramètres, tout comme les fonctions.

```swift
let salut = { (nom: String) in
    print("Salut, \(nom)!")
}
```

Pour appeler cette closure, vous devez passer un argument.

```swift
salut("Jean") // Affiche "Salut, Jean!"
```

## Closure retournant une valeur

Closures as parameters
Trailing closure syntax
Using closures as parameters when they accept parameters
Using closures as parameters when they return values
Shorthand parameter names
Closures with multiple parameters
Returning closures from functions
Capturing values
Closures summary

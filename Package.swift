// swift-tools-version: 6.0
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "HyweeneSiteGenerator",
    platforms: [
        .macOS(.v15)
    ],
    products: [
        // Library product for the main logic (testable)
        .library(
            name: "HyweeneSiteGenerator",
            targets: ["HyweeneSiteGenerator"]
        )
    ],
    dependencies: [
        // Markdown processing
        .package(url: "https://github.com/JohnSundell/Ink.git", from: "0.6.0"),
        // Template engine (Jinja2-like)
        .package(url: "https://github.com/stencilproject/Stencil.git", from: "0.15.1"),
        // YAML parsing
        .package(url: "https://github.com/jpsim/Yams.git", from: "6.2.1"),
        // CLI Arguments parsing (if needed, otherwise we can implement a simple parser)
        .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.7.1"),
    ],
    targets: [
        // Library containing all the logic (testable)
        .target(
            name: "HyweeneSiteGenerator",
            dependencies: [
                .product(name: "Ink", package: "Ink"),
                .product(name: "Stencil", package: "Stencil"),
                .product(name: "Yams", package: "Yams"),
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
            ],
            path: "src/Code",
            exclude: [
                "Application/App/command.swift"
            ],
            sources: ["Application", "Core", "Adapters", "Shared"],
        ),
        // Executable target for the command-line tool
        .executableTarget(
            name: "hyweene",
            dependencies: [
                .target(name: "HyweeneSiteGenerator"),
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
            ],
            path: "src/Code/Application/App",
            exclude: [
                "CLIApp.swift",
                "Commands",
            ],
            sources: ["command.swift"]
        ),
        // Tests, calls the library code
        .testTarget(
            name: "HyweeneSiteGeneratorTests",
            dependencies: [
                .target(name: "HyweeneSiteGenerator")
                //.product(name: "Testing", package: "swift-testing"),
            ],
            path: "src/Tests",
        ),
    ]
)

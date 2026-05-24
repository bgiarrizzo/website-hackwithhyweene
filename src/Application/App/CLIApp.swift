import ArgumentParser

/// Root command for the `hyweene` CLI.
public struct HyweeneCLIApp: AsyncParsableCommand {
    public static let configuration = CommandConfiguration(
        commandName: "hyweene",
        abstract: "Static site generator for hyweene.fr.",
        version: "1.0.0",
        subcommands: [Build.self, Dev.self, QuickAddLink.self, CheckDeadLinks.self]
    )

    public init() {}
}

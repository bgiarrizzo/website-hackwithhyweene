import ArgumentParser

extension HyweeneCLIApp {
    /// Check generated HTML for dead external links.
    public struct CheckDeadLinks: AsyncParsableCommand {
        public static let configuration = CommandConfiguration(
            commandName: "check-dead-links",
            abstract: "Check generated HTML for dead external links."
        )

        @Option(name: .long, help: "Path to scan. Defaults to current release.")
        public var path: String?

        public init() {}

        public mutating func run() async throws {
            try await runCheckDeadLinks(path: path)
        }
    }
}

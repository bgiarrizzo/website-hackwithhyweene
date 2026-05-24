import ArgumentParser

extension HyweeneCLIApp {
    /// Add a curated link from a URL.
    public struct QuickAddLink: AsyncParsableCommand {
        public static let configuration = CommandConfiguration(
            commandName: "quick-add-link",
            abstract: "Add a curated link from a URL."
        )

        @Argument(help: "Absolute URL to fetch.")
        public var url: String

        @Option(name: .long, help: "Optional one-line comment (non-interactive mode).")
        public var comment: String?

        public init() {}

        public mutating func run() async throws {
            try await runQuickAddLink(urlString: url, comment: comment)
        }
    }
}

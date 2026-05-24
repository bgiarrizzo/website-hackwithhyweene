import ArgumentParser

extension HyweeneCLIApp {
    /// Build, serve, and rebuild on changes.
    public struct Dev: AsyncParsableCommand {
        public static let configuration = CommandConfiguration(
            commandName: "dev",
            abstract: "Build, serve, and rebuild on file changes."
        )

        @Option(name: .long, help: "Bind host.")
        public var host: String = "0.0.0.0"

        @Option(name: .long, help: "Bind port (1...65535).")
        public var port: Int = 8000

        public init() {}

        public mutating func validate() throws {
            guard (1...65535).contains(port) else {
                throw ValidationError("--port must be between 1 and 65535.")
            }
        }

        public mutating func run() async throws {
            try await runDevMode(host: host, port: port)
        }
    }
}

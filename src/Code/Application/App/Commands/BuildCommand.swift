import ArgumentParser

extension HyweeneCLIApp {
    /// Build the website once.
    public struct Build: AsyncParsableCommand {
        public static let configuration = CommandConfiguration(
            commandName: "build",
            abstract: "Build the static website once."
        )

        @Flag(
            name: .long,
            help:
                "Copy the release output instead of creating a symbolic link. Use this when running inside a Docker container where symlinks across mount boundaries are not supported."
        )
        public var docker: Bool = false

        public init() {}

        public mutating func run() async throws {
            let isDocker = docker
            _ = try BuildSiteUseCase(buildOperation: { try buildSite(docker: isDocker) }).execute()
        }
    }
}

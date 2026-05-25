import Foundation

/// Raw parsed data for a learning module page.
public struct LearnModulePageDTO: Sendable {
    /// Source file path for diagnostics.
    public let filePath: String
    /// Sort identifier.
    public let id: Int?
    /// Page title.
    public let title: String?
    /// Summary text.
    public let summary: String?
    /// Raw normalized tags.
    public let tags: [String]
    /// Publish date.
    public let publishDate: DateFormat?
    /// Update date.
    public let updateDate: DateFormat?
    /// HTML table of contents.
    public let toc: String
    /// Rendered HTML body.
    public let body: String
    /// Whether Prism assets are required.
    public let prismNeeded: Bool
    /// Disabled flag.
    public let disabled: Bool

    /// Build a DTO from raw parser output.
    public init(from rawData: [String: Any], filePath: String) {
        self.filePath = filePath
        self.id = rawData["id"] as? Int
        self.title = rawData["title"] as? String
        self.summary = rawData["summary"] as? String
        self.tags = Self.parseTags(rawData["tags"])

        // Publish date — Yams may return a String or a Date object
        // We attempt to parse both, but default to nil if parsing fails or the field is absent
        if let str = rawData["publish_date"] as? String {
            // If it's a string, attempt to parse it as a date string
            self.publishDate = DateFormat(from: str) ?? DateFormat()
        } else if let date = rawData["publish_date"] as? Date {
            // If it's already a Date object, convert it to DateFormat
            self.publishDate = DateFormat(date)
        } else {
            // If the field is absent or of an unexpected type, set publishDate to nil
            self.publishDate = nil
        }

        // Update date
        if let str = rawData["update_date"] as? String {
            // If it's a string, attempt to parse it as a date string
            self.updateDate = DateFormat(from: str)
        } else if let date = rawData["update_date"] as? Date {
            // If it's already a Date object, convert it to DateFormat
            self.updateDate = DateFormat(date)
        } else {
            // If the field is absent or of an unexpected type, set updateDate to nil
            self.updateDate = nil
        }

        self.toc = rawData["toc_html"] as? String ?? ""
        self.body = rawData["body"] as? String ?? ""
        self.prismNeeded = rawData["prism_needed"] as? Bool ?? false
        self.disabled = rawData["disabled"] as? Bool ?? false
    }

    private static func parseTags(_ rawValue: Any?) -> [String] {
        if let tags = rawValue as? [String] {
            return tags
        }

        if let tagString = rawValue as? String {
            return
                tagString
                .split(separator: ",")
                .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
                .filter { !$0.isEmpty }
        }

        return []
    }
}

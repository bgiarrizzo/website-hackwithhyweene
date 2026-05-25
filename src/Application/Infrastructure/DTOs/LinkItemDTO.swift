import Foundation

/// Raw data parsed from a links Markdown file.
///
/// Fields remain optional so parsing can represent incomplete frontmatter.
public struct LinkItemDTO: Sendable {
    /// Source file path, used for diagnostics.
    public let filePath: String
    /// Link title from frontmatter.
    public let title: String?
    /// Target URL.
    public let url: String?
    /// Link description.
    public let description: String?
    /// Rendered HTML body.
    public let body: String
    /// Parsed publication date.
    public let publishDate: DateFormat?
    /// Parsed update date.
    public let updateDate: DateFormat?
    /// Pre-computed slug from frontmatter.
    public let slug: String?

    /// Build a DTO from raw parser output.
    public init(from rawData: [String: Any], filePath: String) {
        self.filePath = filePath
        self.title = rawData["title"] as? String
        self.url = rawData["url"] as? String
        self.description = rawData["description"] as? String
        self.body = rawData["body"] as? String ?? ""

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

        self.slug = rawData["slug"] as? String
    }
}

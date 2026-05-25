import Foundation
import Testing

@testable import HyweeneSiteGenerator

struct BlogPostDTOTests {
    // MARK: - Helpers

    let body: String = "<p>TEST Body</p>"
    let filePath: String = "/path/to/post.md"
    let isDraft: Bool = true
    let isNotDraft: Bool = false
    let publishDate: Date = Date(timeIntervalSince1970: 1_700_000_000)
    let publishDateString: String = "2024-01-01"
    let summary: String = "TEST Summary"
    let tags: [String] = ["swift", "testing"]
    let title: String = "TEST Post"
    let updateDate: Date = Date(timeIntervalSince1970: 1_700_000_000)
    let updateDateString: String = "2024-01-02"

    // MARK: - Tests

    @Test("DTO initialises all fields from raw dict")
    func initialisesAllFieldsFromRawDict() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "title": title,
                "summary": summary,
                "publish_date": publishDateString,
            ],
            filePath: filePath
        )

        // Then
        #expect(dto.title == title)
        #expect(dto.summary == summary)
        #expect(dto.publishDate != nil)
    }

    @Test("DTO sets publishDate and updateDate from Date objects")
    func setsPublishDateAndUpdateDateFromDateObjects() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "publish_date": publishDate,
                "update_date": updateDate,
            ],
            filePath: filePath
        )

        // Then
        #expect(dto.publishDate != nil)
        #expect(dto.updateDate != nil)
    }

    @Test("DTO sets nil title when key is absent")
    func setsTitleNilWhenAbsent() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "title": ""
            ],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.title == "")
    }

    @Test("DTO sets nil summary when key is absent")
    func setsSummaryNilWhenAbsent() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "summary": ""
            ],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.summary == "")
    }

    @Test("DTO sets nil publishDate when key is absent")
    func setsPublishDateNilWhenAbsent() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [:],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.publishDate == nil)
    }

    @Test("DTO parses publishDate from Date object (Yams auto-parse)")
    func parsesPublishDateFromDateObject() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "publish_date": publishDate
            ],
            filePath: filePath)

        // Then
        #expect(dto.publishDate != nil)
    }

    @Test("DTO captures tags from raw dict")
    func capturesTagsFromRawDict() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "body": "",
                "tags": tags,
            ],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.tags == tags)
    }

    @Test("DTO defaults tags to empty array when absent")
    func defaultsTagsToEmptyWhenAbsent() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: ["body": ""],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.tags.isEmpty)
    }

    @Test("DTO captures draft flag from raw dict")
    func capturesDraftFlag() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "body": "",
                "draft": isDraft,
            ],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.draft == isDraft)
    }

    @Test("DTO defaults draft to false when absent")
    func defaultsDraftToFalseWhenAbsent() {
        // Given
        let dto: BlogPostDTO = BlogPostDTO(
            from: [
                "body": ""
            ],
            filePath: "/p.md"
        )

        // Then
        #expect(dto.draft == false)
    }
}

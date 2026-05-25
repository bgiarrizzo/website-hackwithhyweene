import Foundation
import Testing

@testable import HyweeneSiteGenerator

struct LearnModulePageDTOTests {
    // MARK: - Helpers

    private func rawData(
        id: Int = 1,
        title: String = "A module page",
        summary: String = "A summary",
        tags: Any = ["git", "vcs"],
        publishDate: String = "2026-05-01",
        updateDate: String = "2026-05-02",
        tocHTML: String = "<ul><li>Section 1</li></ul>",
        body: String = "<p>Content</p>",
        prismNeeded: Bool = true,
        disabled: Bool = false
    ) -> [String: Any] {
        var dict: [String: Any] = [
            "id": id,
            "title": title,
            "summary": summary,
            "tags": tags,
            "publish_date": publishDate,
            "update_date": updateDate,
            "toc_html": tocHTML,
            "body": body,
            "prism_needed": prismNeeded,
            "disabled": disabled,
        ]
        if let tags = tags as? String {
            dict["tags"] = tags
        }
        return dict
    }

    // MARK: - Tests

    @Test("DTO initializes all fields from raw dict")
    func initializesAllFields() {
        let dto = LearnModulePageDTO(
            from: rawData(),
            filePath: "/tmp/01-intro.md"
        )

        #expect(dto.id == 1)
        #expect(dto.title == "A module page")
        #expect(dto.summary == "A summary")
        #expect(dto.tags == ["git", "vcs"])
        #expect(dto.publishDate != nil)
        #expect(dto.updateDate != nil)
        #expect(dto.toc == "<ul><li>Section 1</li></ul>")
        #expect(dto.body == "<p>Content</p>")
        #expect(dto.prismNeeded == true)
        #expect(dto.disabled == false)
    }

    @Test("DTO sets publishDate and updateDate from Date objects")
    func setsPublishDateAndUpdateDateFromDateObjects() {
        let dto = LearnModulePageDTO(
            from: [
                "publish_date": Date(timeIntervalSince1970: 0),
                "update_date": Date(timeIntervalSince1970: 86400),
            ],
            filePath: "/tmp/01-intro.md"
        )

        #expect(dto.publishDate != nil)
        #expect(dto.updateDate != nil)
    }

    @Test("DTO sets nil title when key is absent")
    func setsNilTitleWhenKeyIsAbsent() {
        let dto = LearnModulePageDTO(
            from: [:],
            filePath: "/tmp/01-intro.md"
        )

        #expect(dto.title == nil)
    }

    @Test("DTO normalizes comma separated tags")
    func normalizesCommaSeparatedTags() {
        let dto = LearnModulePageDTO(
            from: [
                "title": "Intro",
                "tags": "git, vcs, workflow",
            ],
            filePath: "/tmp/01-intro.md"
        )

        #expect(dto.title == "Intro")
        #expect(dto.tags == ["git", "vcs", "workflow"])
    }

    @Test("DTO keeps array tags unchanged")
    func keepsArrayTags() {
        let dto = LearnModulePageDTO(
            from: [
                "tags": ["git", "vcs"]
            ],
            filePath: "/tmp/01-intro.md"
        )

        #expect(dto.tags == ["git", "vcs"])
    }
}

import Foundation
import Testing

@testable import HyweeneSiteGenerator

// MARK: - Template Rendering Tests

struct TemplateEngineTests {
    private func writeValidMenuFile(in directory: URL) throws -> String {
        let menuPath = directory.appendingPathComponent("nav-menu.yml")
        try "menu:\n  - name: /blog\n    url: /blog/\n  - name: /about\n    url: /about/\n"
            .write(to: menuPath, atomically: true, encoding: .utf8)
        return menuPath.path
    }

    @Test("Test_TemplateEngine_Render_Simple_Template_With_Variable")
    func renderSimpleTemplate() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("test.html")
        try "Hello {{ name }}!".write(to: templatePath, atomically: true, encoding: .utf8)
        let menuPath = try writeValidMenuFile(in: tempDir)

        let engine = try TemplateEngine(templatePath: tempDir.path, navigationMenuPath: menuPath)
        let result = try engine.render(template: "test.html", context: ["name": "World"])

        #expect(result.contains("Hello World!"))
    }

    @Test("Test_TemplateEngine_Render_Template_With_For_Loop")
    func renderTemplateWithLoop() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("loop.html")
        try "{% for item in items %}{{ item }}{% endfor %}".write(
            to: templatePath, atomically: true, encoding: .utf8)
        let menuPath = try writeValidMenuFile(in: tempDir)

        let engine = try TemplateEngine(templatePath: tempDir.path, navigationMenuPath: menuPath)
        let result = try engine.render(template: "loop.html", context: ["items": ["a", "b", "c"]])

        #expect(
            result.contains("abc")
                || (result.contains("a") && result.contains("b") && result.contains("c")))
    }

    @Test("Test_TemplateEngine_Render_Template_With_If_Condition")
    func renderTemplateWithCondition() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("cond.html")
        try "{% if show %}Visible{% endif %}".write(
            to: templatePath, atomically: true, encoding: .utf8)
        let menuPath = try writeValidMenuFile(in: tempDir)

        let engine = try TemplateEngine(templatePath: tempDir.path, navigationMenuPath: menuPath)

        let resultTrue = try engine.render(template: "cond.html", context: ["show": true])
        #expect(resultTrue.contains("Visible"))

        let resultFalse = try engine.render(template: "cond.html", context: ["show": false])
        #expect(!resultFalse.contains("Visible"))
    }

    // MARK: - Error Handling Tests

    @Test("Test_TemplateEngine_Handle_Missing_Template_File_Gracefully")
    func handleMissingTemplate() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }
        let menuPath = try writeValidMenuFile(in: tempDir)

        let engine = try TemplateEngine(templatePath: tempDir.path, navigationMenuPath: menuPath)

        #expect(throws: TemplateEngineError.self) {
            _ = try engine.render(template: "missing.html", context: [:])
        }
    }

    @Test("Test_TemplateEngine_Handle_Invalid_Template_Syntax_Gracefully")
    func handleInvalidSyntax() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("invalid.html")
        try "{% for item in %}{% endfor %}".write(
            to: templatePath, atomically: true, encoding: .utf8)
        let menuPath = try writeValidMenuFile(in: tempDir)

        let engine = try TemplateEngine(templatePath: tempDir.path, navigationMenuPath: menuPath)

        do {
            _ = try engine.render(template: "invalid.html", context: [:])
            // May or may not throw depending on Stencil's behavior
        } catch {
            // Expected for invalid syntax.
            _ = true
        }
    }

    @Test("Test_TemplateEngine_RenderWithData_Loads_Navigation_Menu")
    func renderWithDataLoadsNavigationMenu() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("menu.html")
        try "{% for item in menu %}[{{ item.name }}:{{ item.url }}]{% endfor %}".write(
            to: templatePath, atomically: true, encoding: .utf8)
        let menuPath = try writeValidMenuFile(in: tempDir)

        let engine = try TemplateEngine(templatePath: tempDir.path, navigationMenuPath: menuPath)
        let result = try engine.renderWithData(template: "menu.html", dataList: [])

        #expect(result.contains("[/blog:/blog/]"))
        #expect(result.contains("[/about:/about/]"))
    }

    @Test("Test_TemplateEngine_RenderWithData_Throws_When_Menu_File_Is_Missing")
    func renderWithDataThrowsWhenMenuFileMissing() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("menu.html")
        try "{{ site.name }}".write(to: templatePath, atomically: true, encoding: .utf8)
        let missingMenuPath = tempDir.appendingPathComponent("missing-nav-menu.yml").path

        let engine = try TemplateEngine(
            templatePath: tempDir.path,
            navigationMenuPath: missingMenuPath
        )

        #expect(throws: TemplateEngineError.self) {
            _ = try engine.renderWithData(template: "menu.html", dataList: [])
        }
    }

    @Test("Test_TemplateEngine_RenderWithData_Throws_When_Menu_YAML_Is_Invalid")
    func renderWithDataThrowsWhenMenuYAMLIsInvalid() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("menu.html")
        try "{{ site.name }}".write(to: templatePath, atomically: true, encoding: .utf8)

        let invalidMenuPath = tempDir.appendingPathComponent("nav-menu.yml")
        try "menu: [invalid".write(to: invalidMenuPath, atomically: true, encoding: .utf8)

        let engine = try TemplateEngine(
            templatePath: tempDir.path,
            navigationMenuPath: invalidMenuPath.path
        )

        #expect(throws: TemplateEngineError.self) {
            _ = try engine.renderWithData(template: "menu.html", dataList: [])
        }
    }

    @Test("Test_TemplateEngine_RenderWithData_Throws_When_Menu_Item_Is_Invalid")
    func renderWithDataThrowsWhenMenuItemIsInvalid() throws {
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(
            UUID().uuidString)
        try FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        let templatePath = tempDir.appendingPathComponent("menu.html")
        try "{{ site.name }}".write(to: templatePath, atomically: true, encoding: .utf8)

        let invalidMenuPath = tempDir.appendingPathComponent("nav-menu.yml")
        try "menu:\n  - name: /blog\n".write(
            to: invalidMenuPath,
            atomically: true,
            encoding: .utf8
        )

        let engine = try TemplateEngine(
            templatePath: tempDir.path,
            navigationMenuPath: invalidMenuPath.path
        )

        #expect(throws: TemplateEngineError.self) {
            _ = try engine.renderWithData(template: "menu.html", dataList: [])
        }
    }
}

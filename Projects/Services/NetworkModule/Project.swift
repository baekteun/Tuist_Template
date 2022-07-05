import ProjectDescription
import ProjectDescriptionHelpers

let project = Project.makeModule(
    name: "NetworkModule",
    product: .staticFramework,
    dependencies: [
        .Project.Module.ThirdPartyLib
    ]
)

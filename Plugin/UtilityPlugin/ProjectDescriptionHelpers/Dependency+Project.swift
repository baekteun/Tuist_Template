import ProjectDescription

public extension TargetDependency {
    struct Project {
        public struct Features {}
        public struct Module {}
        public struct Service {}
        public struct UserInterfaces {}
    }
}

public extension TargetDependency.Project.Features {
    static let CommonFeature = TargetDependency.feature(name: "CommonFeature")
    static let RootFeature = TargetDependency.feature(name: "RootFeature")
}

public extension TargetDependency.Project.Module {
    static let ErrorModule = TargetDependency.module(name: "ErrorModule")
    static let ThirdPartyLib = TargetDependency.module(name: "ThirdPartyLib")
    static let Utility = TargetDependency.module(name: "Utility")
}

public extension TargetDependency.Project.Service {
    static let APIKit = TargetDependency.service(name: "APIKit")
    static let Data = TargetDependency.service(name: "DataModule")
    static let Domain = TargetDependency.service(name: "DomainModule")
    static let DataMappingModule = TargetDependency.service(name: "DataMappingModule")
    static let DatabaseModule = TargetDependency.service(name: "DatabaseModule")
    static let NetworkModule = TargetDependency.service(name: "NetworkModule")
}

public extension TargetDependency.Project.UserInterfaces {
    static let DesignSystem = TargetDependency.ui(name: "DesignSystem")
    static let LocalizableManager = TargetDependency.ui(name: "LocalizableManager")
}

import sys
import os.path
import subprocess

print("Write feature name", end=' : ', flush=True)
feature_name = sys.stdin.readline().replace("\n", "")
print("Include UserInterface? (Y or N, default = Y)", end=' : ', flush=True)
if sys.stdin.readline().replace("\n", "").upper() == "N":
    have_to_make_userinterface = False
else:
    have_to_make_userinterface = True
print("Start to create the feature named " + feature_name)

current_file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_file_path)
os.chdir(os.pardir)
root_path = os.getcwd()
os.chdir(root_path + '/Projects/Features')


def make_clean_mvvm():
    make_root()
    # make_interface()
    make_data_layer()
    make_domain_layer()
    make_presentation_layer()
    if have_to_make_userinterface:
        make_userinterface_layer()


def make_root():
    make_directory(feature_name)


def make_interface():
    dir_name = 'Interface'
    interface_path = feature_name + '/' + dir_name
    sources_path = interface_path + '/Sources'
    tests_path = interface_path + '/Tests'
    layer_directories = [
        interface_path,
        sources_path,
        tests_path
    ]
    make_directories(layer_directories)
    make_project_file(interface_path)
    interface_code = '''
import Foundataion

public protocol ''' + feature_name + '''Interface {
}
'''

    view_paths = [
        ("", 'Interface', interface_code),
    ]

    make_files_at(sources_path, tests_path, view_paths)


def make_data_layer():
    data_source_code = '''
import Foundation
import RxSwift
import UtilityKit

public protocol ''' + feature_name + '''DataSource {
}

public struct ''' + feature_name + '''DataSourceImpl: ''' + feature_name + '''DataSource {
  // MARK: - Initialize
  public init() {
  }

  // MARK: - Implementation
}
'''

    repository_code = '''
import Domain
import Foundation
import InjectPropertyWrapper
import RxSwift
import RxSwiftExt

public struct ''' + feature_name + '''RepositoryImpl: ''' + feature_name + '''Repository {
  // MARK: - Inject
  
  // MARK: - Initialize
  public init() {
  }

  // MARK: - Implementation
  }
}
'''
    model_code = '''
import Foundation
import Domain

public struct <#name#>: Decodable {
}

public extension <#name#> {
    func toEntity() -> <#name#> {
        
    }
    
    static func empty() -> Self {
        
    }
}
'''

    paths = [
        ('DataSources', 'DataSource', data_source_code),
        ('Repositories', 'RepositoryImpl', repository_code),
        ('Models', 'Model', model_code)
    ]
    dependencies = [
        '.Project.Feature.' + feature_name + '.Domain',
        '.Project.Module.CoreKit'
    ]
    make_framework('Data', paths, dependencies=dependencies)


def make_domain_layer():
    repository_code = '''
import Foundation
import RxSwift

public protocol ''' + feature_name + '''Repository {
}
'''
    usecase_code = '''
import Foundation
import InjectPropertyWrapper
import RxSwift

public struct <#name#>: UseCase {
  // MARK: - Parameters
  public typealias Params = Void

  // MARK: - Inject
  @Inject private var repository: ''' + feature_name + '''Repository

  // MARK: - Initialize
  public init() {}

  // MARK: - Implementation
  public func call(params: Void) -> Single<<#type#>> {
  }
}
'''
    entity_code = '''
import Foundation
import UIKit

public struct <#name#> {
  public init() {
  }
} 
'''
    paths = [
        ('Repositories', 'Repository', repository_code),
        ('UseCases', 'UseCase', usecase_code),
        ('Entities', 'Entity', entity_code)
    ]
    dependencies = [
        '.Project.Module.RxPackage'
    ]
    make_framework('Domain', paths, dependencies=dependencies)


def make_presentation_layer():
    router_code = '''
import RxFlow
import RxPackage
import UIKit
import UtilityKit

class ''' + feature_name + '''Flow: Flow {
  var root: Presentable {
    return self.rootViewController
  }

  private lazy var rootViewController: UINavigationController = {
    let viewController = UINavigationController()
    viewController.setNavigationBarHidden(true, animated: false)
    return viewController
  }()

  init() {
  }

  deinit {
    Logger.d("deinit MainFlow")
  }

  func navigate(to step: Step) -> FlowContributors {
    guard let step = step as? AppStep else {
        return .none
    }

    switch step {
    }
  }
}
'''
    view_controller_code = '''
import DesignSystem
import InjectPropertyWrapper
import UIKit

final class ''' + feature_name + '''ViewController: BaseViewController, HasViewModel {
  // MARK: - Constants
  private enum UI {
    enum Color {
      static let navigationBackground: UIColor = .systemBlue
      static let navigationTitle: UIColor = .black
    }
  }
  
  // MARK: - Injection
  @Inject var viewModel: ''' + feature_name + '''ViewModel
  
  // MARK: - UI
  
  // MARK: - View Life Cycle
  public override func loadView() {
  }
  
  override public func viewDidLoad() {
    super.viewDidLoad()
    setupNavigationBar()
    bindUI()
  }
  
  override func setupConstraints() {
  }
}

extension ''' + feature_name + '''ViewController {
  // MARK: - Layout
  private func setupNavigationBar() {
    self.navigationController?.navigationBar.barTintColor = UI.Color.navigationBackground
    self.navigationController?.navigationBar.titleTextAttributes = [.foregroundColor: UI.Color.navigationTitle]
  }
  // MARK: - Configuring
  private func bindUI() {
    
  }
}


// MARK: - Event
extension ''' + feature_name + '''ViewController {
  
}
'''

    viewmodel_code = '''
import Foundation
import RxCocoa
import RxSwift
import RxFlow
import UtilityKit

// You can conform ViewStateManageableProtocols or ViewTransformableProtocols
// If you conform one, you should nonconform Stepper
public final class ''' + feature_name + '''ViewModel: Stepper {
  // MARK: - Properties
  public var steps = PublishRelay<Step>()

  // MARK: - Initialize
  public init() {
  }
}

// MARK: - Bind
extension ''' + feature_name + '''ViewModel {
    
}

// MARK: - UseCase
extension ''' + feature_name + '''ViewModel {
    
}

// MARK: - Route
extension ''' + feature_name + '''ViewModel {
    
}
'''
    paths = [
        ('Routers', 'Flow', router_code),
        ('ViewControllers', 'ViewController', view_controller_code),
        ('ViewModels',  'ViewModel', viewmodel_code)
    ]
    dependencies = [
        '.Project.Feature.' + feature_name + '.Domain',
        '.Project.Feature.' + feature_name + '.UserInterface',
        '.Project.Module.RxPackage',
        '.Project.UserInterface.DesignSystem',
        '.Project.Module.UtilityKit',
        '.Project.UserInterface.LocalizableStringManager',
        '.Project.UserInterface.UserInterfaceLibraryManager'
    ]

    layer_name = 'Presentation'
    make_framework(layer_name, paths, has_demo=True,
                   dependencies=dependencies, is_app_config=True)


def make_userinterface_layer():
    view_code = '''
import ResourcePackage
import SnapKit
import Then
import UIKit

final class ''' + feature_name + '''View: UIView {
  // MARK: - Constants
  private enum UI {
    /// Base

    enum Color {
      static let background: UIColor = R.Color.<#color#>
    }

    enum Font {
    }
  }
  
  // MARK: - UI properties
  
  
  // MARK: - Lifecycle
  override init(frame: CGRect) {
    super.init(frame: frame)
    setupViews()
  }
  
  required init?(coder: NSCoder) {
    fatalError("init(coder:) has not been implemented")
  }
  
  
  private func setupViews() {
    backgroundColor = UI.Color.background
    // TODO: - Setup constraints
  }
}

#if canImport(SwiftUI) && DEBUG
import SwiftUI

@available(iOS 13.0, *)
struct ''' + feature_name + '''Preview: PreviewProvider {
  static var previews: some View {
    UIViewPreview {
      ''' + feature_name + '''View(frame: .zero)
    }.previewDevice(PreviewDevice.init(rawValue: "iPhone 12 Pro"))
  }
}
#endif
'''
    dependencies = [
        '.Project.UserInterface.DesignSystem',
        '.Project.Module.UtilityKit',
        '.Project.UserInterface.LocalizableStringManager',
        '.Project.UserInterface.UserInterfaceLibraryManager'
    ]
    view_paths = [
        ('Views', 'View', view_code),
    ]
    layer_name = 'UserInterface'
    make_framework(layer_name, view_paths, dependencies=dependencies,
                   is_dynamic_framework=True)


def make_framework(layer_name, paths, has_demo=False, dependencies=[], is_dynamic_framework=False, is_app_config=False):
    layer_path = feature_name + '/' + layer_name
    sources_path = layer_path + '/Sources'
    tests_path = layer_path + '/Tests'
    layer_directories = [
        layer_path,
        sources_path,
        tests_path
    ]
    make_directories(layer_directories)
    make_project_file_by(layer_path, has_demo,
                         dependencies, is_dynamic_framework)
    make_files_at(sources_path, tests_path, paths)
    make_xcconfig(feature_name + layer_name, is_app_config)


def make_project_file_by(layer_path, has_demo=False, dependencies=[], is_dynamic_framework=False):
    if is_dynamic_framework:
        make_dynamic_project_file(layer_path, has_demo, dependencies)
    else:
        make_project_file(layer_path, has_demo, dependencies)


def make_files_at(sources_path, tests_path, paths):
    for path_tuple in paths:
        make_source(sources_path, path_tuple[1], path_tuple[2], path_tuple[0])
        make_test(tests_path, path_tuple[1], path_tuple[0])


def make_directories(directories):
    for path in directories:
        make_directory(path)


def make_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def make_project_file(file_path, has_demo=False, dependencies=[]):
    project_file_path = file_path + '/Project.swift'
    file_name = file_path.split('/')[-1]
    command = '''
import ProjectDescription
import ProjectDescriptionHelpers

let project = Project
	.staticFramework(name: "''' + feature_name + file_name + '''",
                   dependencies: [
                    '''
    command += ",\n                    ".join(dependencies)
    if has_demo:
        command += '''
                   ],
                   hasDemoApp: true)'''
    else:
        command += '''
                   ])'''
    write_code_in_file(project_file_path, command)


def make_dynamic_project_file(file_path, has_demo, dependencies):
    project_file_path = file_path + '/Project.swift'
    file_name = file_path.split('/')[-1]
    command = '''
import ProjectDescription
import ProjectDescriptionHelpers

let project = Project
	.framework(name: "''' + feature_name + file_name + '''",
                   dependencies: [
                    '''
    command += ",\n                    ".join(dependencies)
    if has_demo:
        command += '''
                   ],
                   hasDemoApp: true)'''
    else:
        command += '''
                   ])'''
    write_code_in_file(project_file_path, command)


def make_source(file_path, file_name, code, directory_name=""):
    if directory_name == "":
        source_directory_path = file_path
    else:
        source_directory_path = file_path + '/' + directory_name
    make_directory(source_directory_path)

    source_file_path = source_directory_path + \
        '/' + feature_name + file_name + '.swift'
    write_code_in_file(source_file_path, code)


def make_test(file_path, file_name, directory_name=""):
    if directory_name == "":
        source_directory_path = file_path
    else:
        source_directory_path = file_path + '/' + directory_name
    make_directory(source_directory_path)

    source_file_path = source_directory_path + '/' + \
        feature_name + file_name + 'Tests.swift'
    command = '''
import Foundation
import XCTest

public struct ''' + feature_name + file_name + '''Tests: XCTest {
  public init() {}
}
'''
    write_code_in_file(source_file_path, command)


def write_code_in_file(file_path, codes):
    if not os.path.isfile(file_path):
        subprocess.run(['touch', file_path])

    master_key_file = open(file_path, 'w')
    master_key_file.write(codes)
    master_key_file.close()


def write_created_project_structure_on_dependency_project():
    file_path = root_path + \
        "/Plugin/UtilityPlugin/ProjectDescriptionHelpers/Dependency+Project.swift"
    read_file = read_file_at(file_path)
    updated_file = update_file_at(read_file)
    write_file_at(file_path, updated_file)


def read_file_at(file_path):
    with open(file_path, 'r') as file:
        dependecy_project_file = file.readlines()
    return dependecy_project_file


def update_file_at(dependecy_project_file):
    dependecy_project_file_length = len(dependecy_project_file)
    for index, element in enumerate(dependecy_project_file):
        if "struct Module" in element:
            inserting_specific_line = index - 1
            break

    extension_code = '''
public extension TargetDependency.Project.Feature.''' + feature_name + ''' {
    static let Data = TargetDependency.data(name: "''' + feature_name + '''Data")
    static let Domain = TargetDependency.domain(name: "''' + feature_name + '''Domain")
    static let Presentation = TargetDependency.presentation(name: "''' + feature_name + '''Presentation")
    static let UserInterface = TargetDependency.userInterfaceInFeature(name: "''' + feature_name + '''UserInterface")
    static let Pacakge: [TargetDependency] = [Data, Domain, Presentation, UserInterface]
}
'''
    add_structure_in_project_code = '''      public struct ''' + feature_name + ''' {}
'''

    dependecy_project_file.append(extension_code)
    if dependecy_project_file_length > int(inserting_specific_line):
        dependecy_project_file.insert(
            inserting_specific_line, add_structure_in_project_code)

    return dependecy_project_file


def write_file_at(file_path, updated_file):
    with open(file_path, 'w') as file:
        file.writelines(updated_file)


def make_xcconfig(layer_name, is_app_config):
    path = root_path + "/XCConfig/" + layer_name
    make_directory(path)
    if is_app_config:
        make_app_config_file(path)
    else:
        make_config_file(path)


def make_config_file(path):
    code = '#include "../Shared.xcconfig"'
    write_code_in_file(path + "/DEV.xcconfig", code)
    write_code_in_file(path + "/PROD.xcconfig", code)
    write_code_in_file(path + "/TEST.xcconfig", code)


def make_app_config_file(path):
    code = '#include "../App/AppShared-DEV.xcconfig"'
    write_code_in_file(path + "/DEV.xcconfig", code)
    write_code_in_file(path + "/PROD.xcconfig", code)
    write_code_in_file(path + "/TEST.xcconfig", code)


make_clean_mvvm()
write_created_project_structure_on_dependency_project()

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import GeekFanatic.Core 1.0

Rectangle {
    id: activityBar
    color: theme.get_color("activityBar.background")

    // 垂直布局
    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 顶部图标按钮组
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 1

            // 资源管理器
            ActivityBarItem {
                id: explorerButton
                icon.source: "qrc:/icons/explorer.svg"
                icon.color: theme.get_color("activityBar.foreground")
                checked: true
                onClicked: {
                    checked = true
                    filesButton.checked = false
                    searchButton.checked = false
                    extensionsButton.checked = false
                }
            }

            // 搜索
            ActivityBarItem {
                id: searchButton
                icon.source: "qrc:/icons/search.svg"
                icon.color: theme.get_color("activityBar.foreground")
                onClicked: {
                    checked = true
                    explorerButton.checked = false
                    filesButton.checked = false
                    extensionsButton.checked = false
                }
            }

            // 源代码管理
            ActivityBarItem {
                id: filesButton
                icon.source: "qrc:/icons/source-control.svg"
                icon.color: theme.get_color("activityBar.foreground")
                onClicked: {
                    checked = true
                    explorerButton.checked = false
                    searchButton.checked = false
                    extensionsButton.checked = false
                }
            }

            // 扩展
            ActivityBarItem {
                id: extensionsButton
                icon.source: "qrc:/icons/extensions.svg"
                icon.color: theme.get_color("activityBar.foreground")
                onClicked: {
                    checked = true
                    explorerButton.checked = false
                    searchButton.checked = false
                    filesButton.checked = false
                }
            }
        }

        // 底部图标按钮组
        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignBottom
            spacing: 1

            // 设置
            ActivityBarItem {
                id: settingsButton
                icon.source: "qrc:/icons/settings.svg"
                icon.color: theme.get_color("activityBar.foreground")
                onClicked: {
                    // 打开设置
                }
            }
        }
    }

    // 活动栏项组件
    component ActivityBarItem: ToolButton {
        Layout.fillWidth: true
        Layout.preferredHeight: 48
        flat: true
        checkable: true
        
        background: Rectangle {
            color: parent.checked ? theme.get_color("activityBar.activeBackground") 
                                : (parent.hovered ? theme.get_color("activityBar.hoverBackground") 
                                                : "transparent")
        }

        // 左侧选中指示器
        Rectangle {
            visible: parent.checked
            width: 2
            height: parent.height
            color: theme.get_color("activityBar.foreground")
        }

        // 提示文本
        ToolTip {
            visible: parent.hovered
            text: parent.text
            delay: 1000
        }
    }
}
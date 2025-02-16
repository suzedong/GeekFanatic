import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import GeekFanatic.Core 1.0

Rectangle {
    id: sideBar
    color: theme.get_color("sideBar.background")

    // 属性定义
    property string currentView: "explorer"  // 当前视图
    
    // 侧边栏内容
    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 标题栏
        Rectangle {
            Layout.fillWidth: true
            height: 35
            color: theme.get_color("sideBarTitle.background")

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 20
                anchors.rightMargin: 8
                spacing: 4

                // 标题文本
                Label {
                    Layout.fillWidth: true
                    text: {
                        switch (currentView) {
                            case "explorer": return qsTr("资源管理器")
                            case "search": return qsTr("搜索")
                            case "git": return qsTr("源代码管理")
                            case "extensions": return qsTr("扩展")
                            default: return ""
                        }
                    }
                    color: theme.get_color("sideBarTitle.foreground")
                    font.pixelSize: 11
                    elide: Text.ElideRight
                }

                // 操作按钮
                Row {
                    spacing: 4

                    ToolButton {
                        icon.source: "qrc:/icons/more.svg"
                        icon.color: theme.get_color("sideBarTitle.foreground")
                        flat: true
                    }
                }
            }
        }

        // 内容区域
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: {
                switch (currentView) {
                    case "explorer": return 0
                    case "search": return 1
                    case "git": return 2
                    case "extensions": return 3
                    default: return 0
                }
            }

            // 资源管理器视图
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                TreeView {
                    id: explorerTree
                    anchors.fill: parent
                    // TODO: 实现文件树模型
                }
            }

            // 搜索视图
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Column {
                    width: parent.width

                    // 搜索输入框
                    TextField {
                        width: parent.width
                        placeholderText: qsTr("搜索")
                        background: Rectangle {
                            color: theme.get_color("input.background")
                        }
                    }

                    // 搜索结果列表
                    ListView {
                        width: parent.width
                        height: parent.height
                        // TODO: 实现搜索结果模型
                    }
                }
            }

            // Git视图
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Column {
                    width: parent.width
                    // TODO: 实现Git变更列表
                }
            }

            // 扩展视图
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Column {
                    width: parent.width
                    // TODO: 实现扩展列表
                }
            }
        }
    }

    // 分割线
    Rectangle {
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 1
        color: theme.get_color("sideBar.border")

        // 拖动手柄
        MouseArea {
            id: resizeHandle
            anchors.fill: parent
            anchors.margins: -4
            cursorShape: Qt.SplitHCursor
            property real startX
            property real startWidth

            onPressed: {
                startX = mouseX
                startWidth = sideBar.width
            }

            onPositionChanged: {
                if (pressed) {
                    var delta = mouseX - startX
                    var newWidth = Math.max(100, Math.min(800, startWidth + delta))
                    window.set_layout_size("sidebar_width", newWidth)
                }
            }
        }
    }
}
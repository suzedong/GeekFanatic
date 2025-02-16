import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import GeekFanatic.Core 1.0

Rectangle {
    id: panel
    color: theme.get_color("panel.background")
    
    // 属性定义
    property string currentView: "output"  // 当前视图
    property alias panelHeight: panel.height

    // 面板布局
    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 标题栏
        Rectangle {
            id: titleBar
            Layout.fillWidth: true
            height: 35
            color: theme.get_color("panelTitle.background")

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 8
                anchors.rightMargin: 8
                spacing: 4

                // 面板标题列表
                Row {
                    spacing: 1

                    // 问题面板
                    PanelTab {
                        text: qsTr("问题")
                        iconSource: "qrc:/icons/problems.svg"
                        active: currentView === "problems"
                        onClicked: currentView = "problems"
                    }

                    // 输出面板
                    PanelTab {
                        text: qsTr("输出")
                        iconSource: "qrc:/icons/output.svg"
                        active: currentView === "output"
                        onClicked: currentView = "output"
                    }

                    // 终端面板
                    PanelTab {
                        text: qsTr("终端")
                        iconSource: "qrc:/icons/terminal.svg"
                        active: currentView === "terminal"
                        onClicked: currentView = "terminal"
                    }
                }

                Item { Layout.fillWidth: true }

                // 控制按钮
                Row {
                    spacing: 4

                    // 最小化按钮
                    ToolButton {
                        icon.source: "qrc:/icons/minimize.svg"
                        icon.color: theme.get_color("panelTitle.foreground")
                        flat: true
                        onClicked: panel.visible = false
                    }

                    // 最大化切换按钮
                    ToolButton {
                        icon.source: panel.height > 300 ? 
                            "qrc:/icons/restore.svg" : "qrc:/icons/maximize.svg"
                        icon.color: theme.get_color("panelTitle.foreground")
                        flat: true
                        onClicked: {
                            if (panel.height > 300) {
                                window.set_layout_size("panel_height", 200)
                            } else {
                                window.set_layout_size("panel_height", 400)
                            }
                        }
                    }

                    // 关闭按钮
                    ToolButton {
                        icon.source: "qrc:/icons/close.svg"
                        icon.color: theme.get_color("panelTitle.foreground")
                        flat: true
                        onClicked: panel.visible = false
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
                    case "problems": return 0
                    case "output": return 1
                    case "terminal": return 2
                    default: return 1
                }
            }

            // 问题面板
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                ListView {
                    anchors.fill: parent
                    model: ListModel {
                        // TODO: 实现问题列表模型
                    }
                    delegate: ItemDelegate {
                        width: parent.width
                        height: 24
                        
                        contentItem: RowLayout {
                            spacing: 4
                            
                            Image {
                                Layout.preferredWidth: 16
                                Layout.preferredHeight: 16
                                source: model.severity === "error" ? 
                                    "qrc:/icons/error.svg" : "qrc:/icons/warning.svg"
                            }
                            
                            Label {
                                Layout.fillWidth: true
                                text: model.message || ""
                                color: theme.get_color("panel.foreground")
                                elide: Text.ElideRight
                            }
                        }
                    }
                }
            }

            // 输出面板
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                TextArea {
                    anchors.fill: parent
                    readOnly: true
                    color: theme.get_color("panel.foreground")
                    font.family: "Consolas"
                    // TODO: 实现输出内容绑定
                }
            }

            // 终端面板
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: theme.get_color("terminal.background")
                
                // TODO: 实现终端组件
            }
        }
    }

    // 分割线及拖动手柄
    Rectangle {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 1
        color: theme.get_color("panel.border")

        MouseArea {
            id: resizeHandle
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: 8
            cursorShape: Qt.SplitVCursor
            
            property real startY
            property real startHeight
            
            onPressed: {
                startY = mouseY
                startHeight = panel.height
            }
            
            onPositionChanged: {
                if (pressed) {
                    var delta = startY - mouseY
                    var newHeight = Math.max(100, Math.min(800, startHeight + delta))
                    window.set_layout_size("panel_height", newHeight)
                }
            }
        }
    }

    // 面板标签组件
    component PanelTab: Rectangle {
        id: tab
        width: row.width + 16
        height: titleBar.height
        color: active ? theme.get_color("panelTitle.activeBackground") :
                      (hovered ? theme.get_color("panelTitle.hoverBackground") : "transparent")
        
        property bool active: false
        property bool hovered: tabMouse.containsMouse
        property alias text: label.text
        property alias iconSource: icon.source
        signal clicked
        
        Row {
            id: row
            anchors.centerIn: parent
            spacing: 4
            
            Image {
                id: icon
                width: 16
                height: 16
                anchors.verticalCenter: parent.verticalCenter
            }
            
            Label {
                id: label
                anchors.verticalCenter: parent.verticalCenter
                color: active ? theme.get_color("panelTitle.activeForeground") :
                             theme.get_color("panelTitle.inactiveForeground")
                font.pixelSize: 11
            }
        }
        
        MouseArea {
            id: tabMouse
            anchors.fill: parent
            hoverEnabled: true
            onClicked: tab.clicked()
        }
    }
}
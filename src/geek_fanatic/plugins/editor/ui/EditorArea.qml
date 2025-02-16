import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import GeekFanatic.Core 1.0

Rectangle {
    id: editorArea
    color: theme.get_color("editor.background")

    // 属性定义
    property var openFiles: []  // 打开的文件列表
    property int currentIndex: -1  // 当前活动的标签索引

    // 编辑器区域布局
    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 标签栏
        Rectangle {
            id: tabBar
            Layout.fillWidth: true
            height: window.get_layout_size("editor_tabs_height")
            color: theme.get_color("editorGroupHeader.tabsBackground")

            // 标签列表
            ListView {
                id: tabList
                anchors.fill: parent
                orientation: ListView.Horizontal
                clip: true
                model: openFiles
                spacing: 1

                delegate: TabButton {
                    id: tabButton
                    required property int index
                    required property var modelData

                    width: Math.min(200, Math.max(100, implicitWidth))
                    height: tabBar.height
                    text: modelData.fileName || "无标题"
                    checked: index === currentIndex

                    contentItem: RowLayout {
                        spacing: 4

                        // 文件图标
                        Image {
                            Layout.preferredWidth: 16
                            Layout.preferredHeight: 16
                            source: modelData.icon || "qrc:/icons/file.svg"
                        }

                        // 文件名
                        Label {
                            Layout.fillWidth: true
                            text: tabButton.text
                            elide: Text.ElideMiddle
                            color: tabButton.checked ? 
                                theme.get_color("tab.activeForeground") : 
                                theme.get_color("tab.inactiveForeground")
                        }

                        // 关闭按钮
                        ToolButton {
                            Layout.preferredWidth: 16
                            Layout.preferredHeight: 16
                            icon.source: "qrc:/icons/close.svg"
                            icon.color: tabButton.checked ?
                                theme.get_color("tab.activeForeground") :
                                theme.get_color("tab.inactiveForeground")
                            flat: true
                            visible: tabButton.hovered || tabButton.checked

                            onClicked: {
                                closeTab(index)
                            }
                        }
                    }

                    background: Rectangle {
                        color: tabButton.checked ?
                            theme.get_color("tab.activeBackground") :
                            (tabButton.hovered ?
                                theme.get_color("tab.hoverBackground") :
                                theme.get_color("tab.inactiveBackground"))

                        // 活动标签指示器
                        Rectangle {
                            visible: tabButton.checked
                            anchors.top: parent.top
                            width: parent.width
                            height: 2
                            color: theme.get_color("tab.activeBorderTop")
                        }
                    }

                    onClicked: {
                        currentIndex = index
                    }
                }
            }
        }

        // 编辑器堆栈
        StackLayout {
            id: editorStack
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: currentIndex

            // 空编辑器提示
            Rectangle {
                color: theme.get_color("editor.background")

                Column {
                    anchors.centerIn: parent
                    spacing: 20

                    Image {
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: 128
                        height: 128
                        source: "qrc:/icons/geekfanatic.svg"
                        opacity: 0.5
                    }

                    Label {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: qsTr("欢迎使用 GeekFanatic")
                        color: theme.get_color("editor.foreground")
                        font.pixelSize: 24
                    }
                }
            }

            // 动态创建的编辑器实例将被添加到这里
        }
    }

    // 打开新文件
    function openFile(fileInfo) {
        // 检查文件是否已经打开
        let existingIndex = openFiles.findIndex(f => f.path === fileInfo.path)
        if (existingIndex !== -1) {
            currentIndex = existingIndex
            return
        }

        // 创建新的编辑器实例
        let editorComponent = Qt.createComponent("Editor.qml")
        if (editorComponent.status === Component.Ready) {
            let editor = editorComponent.createObject(editorStack, {
                file: fileInfo
            })
            
            // 更新状态
            openFiles.push(fileInfo)
            currentIndex = openFiles.length - 1
        }
    }

    // 关闭标签
    function closeTab(index) {
        if (index >= 0 && index < openFiles.length) {
            // 移除编辑器实例
            let editor = editorStack.itemAt(index)
            if (editor) {
                editor.destroy()
            }

            // 更新状态
            openFiles.splice(index, 1)
            if (currentIndex === index) {
                currentIndex = Math.min(index, openFiles.length - 1)
            } else if (currentIndex > index) {
                currentIndex--
            }
        }
    }
}
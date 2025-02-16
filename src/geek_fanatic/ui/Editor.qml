import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import GeekFanatic.Core 1.0

Rectangle {
    id: editor
    color: theme.get_color("editor.background")

    // 属性定义
    property var file: null  // 文件信息
    property alias text: textArea.text
    property alias modified: textArea.modified
    property int currentLine: 1
    property int currentColumn: 1

    // 编辑器布局
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // 行号区域
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: lineNumbers.width + 20
            color: theme.get_color("editorGutter.background")

            Column {
                id: lineNumbers
                y: -textArea.flickableItem.contentY
                width: metrics.width
                spacing: 0

                Repeater {
                    model: textArea.lineCount

                    delegate: Text {
                        required property int index
                        width: metrics.width
                        height: textArea.fontMetrics.height
                        horizontalAlignment: Text.AlignRight
                        text: index + 1
                        color: theme.get_color("editorLineNumber.foreground")
                        font: textArea.font
                        opacity: currentLine === (index + 1) ? 1.0 : 0.5
                    }
                }
            }

            // 用于计算行号宽度的文本度量
            TextMetrics {
                id: metrics
                font: textArea.font
                text: textArea.lineCount.toString()
            }
        }

        // 编辑器区域
        ScrollView {
            id: scrollView
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            TextArea {
                id: textArea
                anchors.fill: parent
                color: theme.get_color("editor.foreground")
                selectionColor: theme.get_color("editor.selectionBackground")
                selectedTextColor: theme.get_color("editor.selectionForeground")
                font.family: "Consolas"
                font.pixelSize: 13
                wrapMode: TextEdit.NoWrap
                selectByMouse: true
                persistentSelection: true
                
                property bool modified: false
                property int lineCount: text.split('\n').length
                property var fontMetrics: TextMetrics {
                    font: textArea.font
                    text: "M"  // 用于计算行高的参考字符
                }

                // 显示当前行高亮
                Rectangle {
                    id: currentLineHighlight
                    width: scrollView.width
                    height: textArea.fontMetrics.height
                    y: (currentLine - 1) * textArea.fontMetrics.height - textArea.flickableItem.contentY
                    color: theme.get_color("editor.lineHighlightBackground")
                    opacity: 0.5
                }

                // 光标位置变更处理
                onCursorPositionChanged: {
                    var pos = cursorPosition
                    var text = textArea.text.substring(0, pos)
                    var lastNewline = text.lastIndexOf("\n")
                    var lineStartPos = lastNewline === -1 ? 0 : lastNewline + 1
                    
                    currentLine = text.split('\n').length
                    currentColumn = pos - lineStartPos + 1

                    // 发送光标位置变更信号
                    core.cursorPositionChanged(currentLine, currentColumn)
                }

                // 内容变更处理
                onTextChanged: {
                    modified = true
                    // TODO: 实现自动保存功能
                }

                // 按键处理
                Keys.onPressed: (event) => {
                    // Tab键处理
                    if (event.key === Qt.Key_Tab) {
                        insert(cursorPosition, "    ")
                        event.accepted = true
                    }
                }

                // 上下文菜单
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    propagateComposedEvents: true

                    onClicked: (mouse) => {
                        if (mouse.button === Qt.RightButton) {
                            contextMenu.popup()
                        }
                    }
                }

                Menu {
                    id: contextMenu

                    MenuItem {
                        text: qsTr("撤销")
                        enabled: textArea.canUndo
                        onTriggered: textArea.undo()
                    }
                    MenuItem {
                        text: qsTr("重做")
                        enabled: textArea.canRedo
                        onTriggered: textArea.redo()
                    }
                    MenuSeparator {}
                    MenuItem {
                        text: qsTr("剪切")
                        enabled: textArea.selectedText
                        onTriggered: textArea.cut()
                    }
                    MenuItem {
                        text: qsTr("复制")
                        enabled: textArea.selectedText
                        onTriggered: textArea.copy()
                    }
                    MenuItem {
                        text: qsTr("粘贴")
                        enabled: textArea.canPaste
                        onTriggered: textArea.paste()
                    }
                    MenuSeparator {}
                    MenuItem {
                        text: qsTr("全选")
                        onTriggered: textArea.selectAll()
                    }
                }
            }
        }
    }

    // 加载文件内容
    function loadFile() {
        if (file && file.path) {
            // TODO: 通过插件系统加载文件内容
            textArea.text = "// TODO: 加载文件内容\n"
            textArea.modified = false
        }
    }

    // 保存文件内容
    function saveFile() {
        if (file && file.path) {
            // TODO: 通过插件系统保存文件内容
            textArea.modified = false
        }
    }

    Component.onCompleted: {
        loadFile()
    }
}
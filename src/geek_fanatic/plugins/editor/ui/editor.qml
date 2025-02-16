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

                    delegate: Row {
                        required property int index
                        width: metrics.width + foldingIndicator.width
                        height: textArea.fontMetrics.height
                        spacing: 4

                        // 折叠指示器
                        Item {
                            id: foldingIndicator
                            width: 12
                            height: parent.height
                            visible: {
                                if (!textArea.editorInstance) return false
                                var folding = textArea.editorInstance.get_feature("folding")
                                return folding ? folding.is_foldable_line(index + 1) : false
                            }

                            Rectangle {
                                anchors.centerIn: parent
                                width: 8
                                height: 8
                                radius: 1
                                color: "transparent"
                                border.color: theme.get_color("editorGutter.foldingControlForeground")
                                border.width: 1

                                // 折叠状态指示
                                Rectangle {
                                    anchors.centerIn: parent
                                    width: parent.width - 2
                                    height: 1
                                    color: parent.border.color

                                    // 垂直线(展开状态)
                                    Rectangle {
                                        anchors.centerIn: parent
                                        width: 1
                                        height: parent.width
                                        color: parent.color
                                        visible: {
                                            if (!textArea.editorInstance) return true
                                            var folding = textArea.editorInstance.get_feature("folding")
                                            return folding ? !folding.is_folded(index + 1) : true
                                        }

                                        // 展开/收起动画
                                        Behavior on height {
                                            NumberAnimation {
                                                duration: 200
                                                easing.type: Easing.InOutQuad
                                            }
                                        }
                                    }
                                }
                            }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    if (!textArea.editorInstance) return
                                    var folding = textArea.editorInstance.get_feature("folding")
                                    if (folding) {
                                        if (folding.is_folded(index + 1)) {
                                            folding.unfold(index + 1)
                                        } else {
                                            folding.fold(index + 1)
                                        }
                                    }
                                }
                            }
                        }

                        // 行号文本
                        Text {
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

                // 绑定到后端编辑器实例
                property var editorInstance: null

                // 动画定义
                Behavior on contentY {
                    NumberAnimation { duration: 200; easing.type: Easing.OutCubic }
                }

                // 光标位置变更处理
                onCursorPositionChanged: {
                    if (!editorInstance) return
                    
                    var pos = cursorPosition
                    var text = textArea.text.substring(0, pos)
                    var lastNewline = text.lastIndexOf("\n")
                    var lineStartPos = lastNewline === -1 ? 0 : lastNewline + 1
                    
                    currentLine = text.split('\n').length
                    currentColumn = pos - lineStartPos + 1

                    // 更新后端编辑器状态
                    editorInstance.set_cursor_position(currentLine, currentColumn)
                }

                // 内容变更处理
                onTextChanged: {
                    if (!editorInstance) return
                    
                    modified = true
                    editorInstance.set_content(text)
                }

                // 选中文本变更处理
                onSelectedTextChanged: {
                    if (!editorInstance || !selectedText) {
                        editorInstance.clear_selection()
                        return
                    }
                    
                    var selStart = selectionStart
                    var selEnd = selectionEnd
                    var startText = text.substring(0, selStart)
                    var endText = text.substring(0, selEnd)
                    
                    var startLine = startText.split('\n').length
                    var endLine = endText.split('\n').length
                    var startCol = selStart - startText.lastIndexOf("\n") - 1
                    var endCol = selEnd - endText.lastIndexOf("\n") - 1
                    
                    editorInstance.set_selection(startLine, startCol, endLine, endCol)
                }

                // 连接后端信号
                Connections {
                    target: editorInstance
                    
                    function onContentChanged() {
                        var content = editorInstance.content
                        if (content !== textArea.text) {
                            textArea.text = content
                        }
                    }
                    
                    function onCursorPositionChanged(line, column) {
                        if (line !== currentLine || column !== currentColumn) {
                            // TODO: 实现光标位置同步
                        }
                    }
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
        if (!file || !file.path) return

        // 通过编辑器插件加载文件
        var editorPlugin = core.plugin_manager.get_plugin("geekfanatic.editor")
        if (editorPlugin) {
            // 创建编辑器实例
            textArea.editorInstance = editorPlugin.create_editor()
            
            // 加载文件内容
            var content = editorPlugin.read_file(file.path)
            if (content) {
                textArea.text = content
                textArea.modified = false
            }
            
            // 初始化语法高亮
            var fileType = file.path.split('.').pop()
            var highlighter = textArea.editorInstance.get_feature("highlight")
            if (highlighter) {
                highlighter.set_language(fileType)
            }
            
            // 初始化代码折叠
            var folding = textArea.editorInstance.get_feature("folding")
            if (folding) {
                folding.scan_foldable_regions()
            }
        }
    }

    // 保存文件内容
    function saveFile() {
        if (!file || !file.path) return
        
        // 通过编辑器插件保存文件
        var editorPlugin = core.plugin_manager.get_plugin("geekfanatic.editor")
        if (editorPlugin) {
            editorPlugin.write_file(file.path, textArea.text)
            textArea.modified = false
            
            // 更新语法高亮
            var highlighter = textArea.editorInstance.get_feature("highlight")
            if (highlighter) {
                highlighter.refresh()
            }
        }
    }

    Component.onCompleted: {
        loadFile()
    }
}
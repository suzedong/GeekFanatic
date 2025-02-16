import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import GeekFanatic.Core 1.0

Rectangle {
    id: statusBar
    color: theme.get_color("statusBar.background")

    // 状态栏布局
    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 8
        anchors.rightMargin: 8
        spacing: 8

        // 左侧状态项
        Row {
            spacing: 12

            // 分支信息
            StatusBarItem {
                icon.source: "qrc:/icons/git-branch.svg"
                text: "main"
                tooltip: qsTr("当前 Git 分支")
            }

            // 问题计数
            StatusBarItem {
                icon.source: "qrc:/icons/error.svg"
                text: "0  0"
                tooltip: qsTr("错误数 0, 警告数 0")
            }
        }

        Item { Layout.fillWidth: true }  // 弹性空间

        // 右侧状态项
        Row {
            spacing: 12

            // 编码格式
            StatusBarItem {
                text: "UTF-8"
                tooltip: qsTr("选择编码格式")
            }

            // 行尾序列
            StatusBarItem {
                text: "CRLF"
                tooltip: qsTr("选择行尾序列")
            }

            // 语言模式
            StatusBarItem {
                text: "Python"
                tooltip: qsTr("选择语言模式")
            }

            // 缩进设置
            StatusBarItem {
                text: "空格: 4"
                tooltip: qsTr("选择缩进设置")
            }

            // 光标位置
            StatusBarItem {
                text: "第 1 行，第 1 列"
                tooltip: qsTr("转到行/列")
            }
        }
    }

    // 状态栏项组件
    component StatusBarItem: Rectangle {
        id: item
        height: statusBar.height
        width: row.width + 16
        color: itemMouse.containsMouse ? 
            theme.get_color("statusBar.hoverBackground") : "transparent"

        property alias icon: itemIcon
        property alias text: itemText.text
        property alias tooltip: itemTooltip.text

        Row {
            id: row
            anchors.centerIn: parent
            spacing: 4

            Image {
                id: itemIcon
                visible: status === Image.Ready
                width: 16
                height: 16
                anchors.verticalCenter: parent.verticalCenter
                sourceSize: Qt.size(16, 16)
            }

            Label {
                id: itemText
                anchors.verticalCenter: parent.verticalCenter
                color: theme.get_color("statusBar.foreground")
                font.pixelSize: 11
            }
        }

        MouseArea {
            id: itemMouse
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }

        ToolTip {
            id: itemTooltip
            visible: itemMouse.containsMouse && text
            delay: 1000
        }
    }

    // 分割线
    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 1
        color: theme.get_color("statusBar.border")
    }

    // 信号处理
    Connections {
        target: core

        function onStatusMessageChanged(message) {
            // TODO: 更新状态消息
        }

        function onCursorPositionChanged(line, column) {
            // TODO: 更新光标位置
        }

        function onFileEncodingChanged(encoding) {
            // TODO: 更新文件编码
        }
    }
}
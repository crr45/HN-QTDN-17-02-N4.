odoo.define('quan_ly_van_ban.ChatbotSystray', function (require) {
    "use strict";

    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var QWeb = core.qweb;

    var ChatbotSystray = Widget.extend({
        template: 'quan_ly_van_ban.ChatbotSystrayIcon',
        events: {
            'click .o_chatbot_icon': '_onToggleChat',
        },
        init: function () {
            this._super.apply(this, arguments);
            this.isOpen = false;
        },
        start: function () {
            var self = this;
            this._super.apply(this, arguments);
            
            // Render the chat window and append to body
            this.$chatContainer = $(QWeb.render('quan_ly_van_ban.ChatbotWindow', {}));
            $('body').append(this.$chatContainer);
            this.$chatContainer.hide();
            
            // Bind header events
            this.$chatContainer.find('.chatbot-close').click(function () {
                self._onToggleChat();
            });
            this.$chatContainer.find('.chatbot-send').click(function () {
                self._onSendMessage();
            });
            this.$chatContainer.find('.chatbot-input').keypress(function (e) {
                if (e.which === 13) {
                    self._onSendMessage();
                }
            });
            
            // Load a friendly welcome message
            this._addMessage('Chào bạn! Tôi là Trợ lý AI tích hợp. Bạn có câu hỏi nào về khách hàng, nhân viên hay văn bản trong hệ thống không?', 'assistant');
        },
        _onToggleChat: function () {
            this.isOpen = !this.isOpen;
            if (this.isOpen) {
                this.$chatContainer.fadeIn();
                this.$chatContainer.find('.chatbot-input').focus();
            } else {
                this.$chatContainer.fadeOut();
            }
        },
        _addMessage: function (text, sender) {
            var $msgList = this.$chatContainer.find('.chatbot-messages');
            var $msg = $('<div class="chatbot-message ' + sender + '"><div class="msg-content">' + text + '</div></div>');
            $msgList.append($msg);
            $msgList.scrollTop($msgList[0].scrollHeight);
        },
        _onSendMessage: function () {
            var self = this;
            var $input = this.$chatContainer.find('.chatbot-input');
            var text = $input.val().trim();
            if (!text) return;
            
            $input.val('');
            this._addMessage(text, 'user');
            
            // Render Typing/thinking indicator
            var $typing = $('<div class="chatbot-message assistant typing"><div class="msg-content"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>');
            var $msgList = this.$chatContainer.find('.chatbot-messages');
            $msgList.append($typing);
            $msgList.scrollTop($msgList[0].scrollHeight);
            
            this._rpc({
                route: '/chatbot/message',
                params: {
                    message: text
                }
            }).then(function (res) {
                $typing.remove();
                if (res && res.status === 'success') {
                    self._addMessage(res.reply, 'assistant');
                } else {
                    self._addMessage(res.reply || 'Có lỗi xảy ra khi liên kết với trợ lý AI.', 'assistant');
                }
            }).catch(function (err) {
                $typing.remove();
                self._addMessage('Lỗi kết nối tới máy chủ.', 'assistant');
            });
        }
    });

    SystrayMenu.Items.push(ChatbotSystray);
    return ChatbotSystray;
});

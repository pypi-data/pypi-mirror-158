/* http://keith-wood.name/calendars.html
   Simplified Chinese localisation for Gregorian/Julian calendars for jQuery.
   Written by Cloudream (cloudream@gmail.com). */
(function($) {
	'use strict';
	$.calendars.calendars.gregorian.prototype.regionalOptions['zh-CN'] = {
		name: 'Gregorian',
		epochs: ['BCE', 'CE'],
		monthNames: ['一月','二月','三月','四月','五月','六月',
		'七月','八月','九月','十月','十一月','十二月'],
		monthNamesShort: ['一','二','三','四','五','六',
		'七','八','九','十','十一','十二'],
		dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
		dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
		dayNamesMin: ['日','一','二','三','四','五','六'],
		digits: $.calendars.substituteChineseDigits(
			['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'], ['', '十', '百', '千']),
		dateFormat: 'yyyy-mm-dd',
		firstDay: 1,
		isRTL: false
	};
	if ($.calendars.calendars.julian) {
		$.calendars.calendars.julian.prototype.regionalOptions['zh-CN'] =
			$.calendars.calendars.gregorian.prototype.regionalOptions['zh-CN'];
	}
})(jQuery);

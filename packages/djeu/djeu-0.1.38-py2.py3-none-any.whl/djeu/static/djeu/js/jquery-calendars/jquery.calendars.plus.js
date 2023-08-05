﻿/* http://keith-wood.name/calendars.html
   Calendars extras for jQuery v2.1.0.
   Written by Keith Wood (wood.keith{at}optusnet.com.au) August 2009.
   Available under the MIT (http://keith-wood.name/licence.html) license. 
   Please attribute the author if you use it. */

(function($) { // Hide scope, no $ conflict
	'use strict';

	$.extend($.calendars.regionalOptions[''], {
		invalidArguments: 'Invalid arguments',
		invalidFormat: 'Cannot format a date from another calendar',
		missingNumberAt: 'Missing number at position {0}',
		unknownNameAt: 'Unknown name at position {0}',
		unexpectedLiteralAt: 'Unexpected literal at position {0}',
		unexpectedText: 'Additional text found at end'
	});
	$.calendars.local = $.calendars.regionalOptions[''];

	$.extend($.calendars.cdate.prototype, {

		/** Format this date.
			Found in the <code>jquery.calendars.plus.js</code> module.
			@memberof CDate
			@param {string} [format] The date format to use (see {@linkcode BaseCalendar.formatDate|formatDate}).
			@param {object} [settings] Options for the <code>formatDate</code> function.
			@return {string} The formatted date. */
		formatDate: function(format, settings) {
			if (typeof format !== 'string') {
				settings = format;
				format = '';
			}
			return this._calendar.formatDate(format || '', this, settings);
		}
	});

	$.extend($.calendars.baseCalendar.prototype, {

		UNIX_EPOCH: $.calendars.instance().newDate(1970, 1, 1).toJD(),
		SECS_PER_DAY: 24 * 60 * 60,
		TICKS_EPOCH: $.calendars.instance().jdEpoch, // 1 January 0001 CE
		TICKS_PER_DAY: 24 * 60 * 60 * 10000000,

		/** Date format for ATOM (RFC 3339/ISO 8601) - 'yyyy-mm-dd'.
			@memberof BaseCalendar */
		ATOM: 'yyyy-mm-dd',
		/** Date format for cookies - 'D, dd M yyyy'.
			@memberof BaseCalendar */
		COOKIE: 'D, dd M yyyy',
		/** Date format for the full date - 'DD, MM d, yyyy'.
			@memberof BaseCalendar */
		FULL: 'DD, MM d, yyyy',
		/** Date format for ISO 8601 - 'yyyy-mm-dd'.
			@memberof BaseCalendar */
		ISO_8601: 'yyyy-mm-dd',
		/** Date format for Julian date - days since January 1, 4713 BCE Greenwich noon.
			@memberof BaseCalendar */
		JULIAN: 'J',
		/** Date format for RFC 822 - 'D, d M yy'.
			@memberof BaseCalendar */
		RFC_822: 'D, d M yy',
		/** Date format for RFC 850 - 'DD, dd-M-yy'.
			@memberof BaseCalendar */
		RFC_850: 'DD, dd-M-yy',
		/** Date format for RFC 1036 - 'D, d M yy'.
			@memberof BaseCalendar */
		RFC_1036: 'D, d M yy',
		/** Date format for RFC 1123 - 'D, d M yyyy'.
			@memberof BaseCalendar */
		RFC_1123: 'D, d M yyyy',
		/** Date format for RFC 2822 - 'D, d M yyyy'.
			@memberof BaseCalendar */
		RFC_2822: 'D, d M yyyy',
		/** Date format for RSS (RFC 822) - 'D, d M yy'.
			@memberof BaseCalendar */
		RSS: 'D, d M yy',
		/** Date format for Windows ticks - number of 100-nanosecond ticks since 1 January 0001 00:00:00 UTC.
			@memberof BaseCalendar */
		TICKS: '!',
		/** Date format for Unix timestamp - number of seconds elapsed since the
			start of the Unix epoch at 1 January 1970 00:00:00 UTC.
			@memberof BaseCalendar */
		TIMESTAMP: '@',
		/** Date format for W3C (ISO 8601) - 'yyyy-mm-dd'.
			@memberof BaseCalendar */
		W3C: 'yyyy-mm-dd',

		/** Format a date object into a string value.
			The format can be combinations of the following:
			<ul>
			<li>d  - day of month (no leading zero)</li>
			<li>dd - day of month (two digit)</li>
			<li>o  - day of year (no leading zeros)</li>
			<li>oo - day of year (three digit)</li>
			<li>D  - day name short</li>
			<li>DD - day name long</li>
			<li>w  - week of year (no leading zero)</li>
			<li>ww - week of year (two digit)</li>
			<li>m  - month of year (no leading zero)</li>
			<li>mm - month of year (two digit)</li>
			<li>M  - month name short</li>
			<li>MM - month name long</li>
			<li>yy - year (two digit)</li>
			<li>yyyy - year (four digit)</li>
			<li>YYYY - formatted year</li>
			<li>J  - Julian date (days since January 1, 4713 BCE Greenwich noon)</li>
			<li>@  - Unix timestamp (s since 01/01/1970)</li>
			<li>!  - Windows ticks (100ns since 01/01/0001)</li>
			<li>'...' - literal text</li>
			<li>'' - single quote</li>
			</ul>
			Found in the <code>jquery.calendars.plus.js</code> module.
			@memberof BaseCalendar
			@param {string} [format] The desired format of the date (defaults to calendar format).
			@param {CDate} date The date value to format.
			@param {object} [settings] Addition options, whose attributes include:
			@param {string[]} [settings.dayNamesShort] Abbreviated names of the days from day 0 (Sunday).
			@param {string[]} [settings.dayNames] Names of the days from day 0 (Sunday).
			@param {string[]} [settings.monthNamesShort] Abbreviated names of the months.
			@param {string[]} [settings.monthNames] Names of the months.
			@param {boolean} [settings.localNumbers=false] <code>true</code> to localise numbers (if available),
				<code>false</code> to use normal Arabic numerals.
			@return {string} The date in the above format.
			@throws Errors if the date is from a different calendar. */
		formatDate: function(format, date, settings) {
			if (typeof format !== 'string') {
				settings = date;
				date = format;
				format = '';
			}
			if (!date) {
				return '';
			}
			if (date.calendar() !== this) {
				throw $.calendars.local.invalidFormat || $.calendars.regionalOptions[''].invalidFormat;
			}
			format = format || this.local.dateFormat;
			settings = settings || {};
			var dayNamesShort = settings.dayNamesShort || this.local.dayNamesShort;
			var dayNames = settings.dayNames || this.local.dayNames;
			var monthNamesShort = settings.monthNamesShort || this.local.monthNamesShort;
			var monthNames = settings.monthNames || this.local.monthNames;
			var localNumbers = settings.localNumbers || this.local.localNumbers;
			// Check whether a format character is doubled
			var doubled = function(match, step) {
				var matches = 1;
				while (iFormat + matches < format.length && format.charAt(iFormat + matches) === match) {
					matches++;
				}
				iFormat += matches - 1;
				return Math.floor(matches / (step || 1)) > 1;
			};
			// Format a number, with leading zeroes if necessary
			var formatNumber = function(match, value, len, step) {
				var num = '' + value;
				if (doubled(match, step)) {
					while (num.length < len) {
						num = '0' + num;
					}
				}
				return num;
			};
			// Format a name, short or long as requested
			var formatName = function(match, value, shortNames, longNames) {
				return (doubled(match) ? longNames[value] : shortNames[value]);
			};
			// Localise numbers if requested and available
			var localiseNumbers = localNumbers && this.local.digits ?
				this.local.digits : function(value) { return value; };
			var output = '';
			var literal = false;
			for (var iFormat = 0; iFormat < format.length; iFormat++) {
				if (literal) {
					if (format.charAt(iFormat) === '\'' && !doubled('\'')) {
						literal = false;
					}
					else {
						output += format.charAt(iFormat);
					}
				}
				else {
					switch (format.charAt(iFormat)) {
						case 'd':
							output += localiseNumbers(formatNumber('d', date.day(), 2));
							break;
						case 'D':
							output += formatName('D', date.dayOfWeek(), dayNamesShort, dayNames);
							break;
						case 'o':
							output += formatNumber('o', date.dayOfYear(), 3);
							break;
						case 'w':
							output += formatNumber('w', date.weekOfYear(), 2);
							break;
						case 'm':
							output += localiseNumbers(formatNumber('m', date.month(), 2));
							break;
						case 'M':
							output += formatName('M', date.month() - this.minMonth, monthNamesShort, monthNames);
							break;
						case 'y':
							output += localiseNumbers(doubled('y', 2) ? date.year() :
								(date.year() % 100 < 10 ? '0' : '') + date.year() % 100);
							break;
						case 'Y':
							doubled('Y', 2);
							output += date.formatYear();
							break;
						case 'J':
							output += date.toJD();
							break;
						case '@':
							output += (date.toJD() - this.UNIX_EPOCH) * this.SECS_PER_DAY;
							break;
						case '!':
							output += (date.toJD() - this.TICKS_EPOCH) * this.TICKS_PER_DAY;
							break;
						case '\'':
							if (doubled('\'')) {
								output += '\'';
							}
							else {
								literal = true;
							}
							break;
						default:
							output += format.charAt(iFormat);
					}
				}
			}
			return output;
		},

		/** Parse a string value into a date object.
			See {@linkcode BaseCalendar.formatDate|formatDate} for the possible formats, plus:
			<ul>
			<li>* - ignore rest of string</li>
			</ul>
			Found in the <code>jquery.calendars.plus.js</code> module.
			@memberof BaseCalendar
			@param {string} format The expected format of the date ('' for default calendar format).
			@param {string} value The date in the above format.
			@param {object} [settings] Additional options whose attributes include:
			@param {number} [settings.shortYearCutoff] The cutoff year for determining the century.
			@param {string[]} [settings.dayNamesShort] Abbreviated names of the days from day 0 (Sunday).
			@param {string[]} [settings.dayNames] Names of the days from day 0 (Sunday).
			@param {string[]} [settings.monthNamesShort] Abbreviated names of the months.
			@param {string[]} [settings.monthNames] Names of the months.
			@return {CDate} The extracted date value or <code>null</code> if value is blank.
			@throws Errors if the format and/or value are missing,
					if the value doesn't match the format, or if the date is invalid. */
		parseDate: function(format, value, settings) {
			if (typeof value === 'undefined' || value === null) {
				throw $.calendars.local.invalidArguments || $.calendars.regionalOptions[''].invalidArguments;
			}
			value = (typeof value === 'object' ? value.toString() : value + '');
			if (value === '') {
				return null;
			}
			format = format || this.local.dateFormat;
			settings = settings || {};
			var shortYearCutoff = settings.shortYearCutoff || this.shortYearCutoff;
			shortYearCutoff = (typeof shortYearCutoff !== 'string' ? shortYearCutoff :
				this.today().year() % 100 + parseInt(shortYearCutoff, 10));
			var dayNamesShort = settings.dayNamesShort || this.local.dayNamesShort;
			var dayNames = settings.dayNames || this.local.dayNames;
			var monthNamesShort = settings.monthNamesShort || this.local.monthNamesShort;
			var monthNames = settings.monthNames || this.local.monthNames;
			var jd = -1;
			var year = -1;
			var month = -1;
			var day = -1;
			var doy = -1;
			var shortYear = false;
			var literal = false;
			// Check whether a format character is doubled
			var doubled = function(match, step) {
				var matches = 1;
				while (iFormat + matches < format.length && format.charAt(iFormat + matches) === match) {
					matches++;
				}
				iFormat += matches - 1;
				return Math.floor(matches / (step || 1)) > 1;
			};
			// Extract a number from the string value
			var getNumber = function(match, step) {
				var isDoubled = doubled(match, step);
				var size = [2, 3, isDoubled ? 4 : 2, isDoubled ? 4 : 2, 10, 11, 20]['oyYJ@!'.indexOf(match) + 1];
				var digits = new RegExp('^-?\\d{1,' + size + '}');
				var num = value.substring(iValue).match(digits);
				if (!num) {
					throw ($.calendars.local.missingNumberAt || $.calendars.regionalOptions[''].missingNumberAt).
						replace(/\{0\}/, iValue);
				}
				iValue += num[0].length;
				return parseInt(num[0], 10);
			};
			// Extract a name from the string value and convert to an index
			var calendar = this;
			var getName = function(match, shortNames, longNames, step) {
				var names = (doubled(match, step) ? longNames : shortNames);
				var index = -1;
				for (var i = 0; i < names.length; i++) {
					if (value.substr(iValue, names[i].length).toLowerCase() === names[i].toLowerCase()) {
						if (index === -1) {
							index = i;
						} else if (names[i].length > names[index].length) {
							index = i;
						}
					}
				}
				if (index > -1) {
					iValue += names[index].length;
					return index + calendar.minMonth;
				}
				throw ($.calendars.local.unknownNameAt || $.calendars.regionalOptions[''].unknownNameAt).
					replace(/\{0\}/, iValue);
			};
			// Confirm that a literal character matches the string value
			var checkLiteral = function() {
				if (value.charAt(iValue) !== format.charAt(iFormat)) {
					throw ($.calendars.local.unexpectedLiteralAt ||
						$.calendars.regionalOptions[''].unexpectedLiteralAt).replace(/\{0\}/, iValue);
				}
				iValue++;
			};
			var iValue = 0;
			for (var iFormat = 0; iFormat < format.length; iFormat++) {
				if (literal) {
					if (format.charAt(iFormat) === '\'' && !doubled('\'')) {
						literal = false;
					}
					else {
						checkLiteral();
					}
				}
				else {
					switch (format.charAt(iFormat)) {
						case 'd':
							day = getNumber('d');
							break;
						case 'D':
							getName('D', dayNamesShort, dayNames);
							break;
						case 'o':
							doy = getNumber('o');
							break;
						case 'w':
							getNumber('w');
							break;
						case 'm':
							month = getNumber('m');
							break;
						case 'M':
							month = getName('M', monthNamesShort, monthNames);
							break;
						case 'y':
							var iSave = iFormat;
							shortYear = !doubled('y', 2);
							iFormat = iSave;
							year = getNumber('y', 2);
							break;
						case 'Y':
							year = getNumber('Y', 2);
							break;
						case 'J':
							jd = getNumber('J') + 0.5;
							if (value.charAt(iValue) === '.') {
								iValue++;
								getNumber('J');
							}
							break;
						case '@':
							jd = getNumber('@') / this.SECS_PER_DAY + this.UNIX_EPOCH;
							break;
						case '!':
							jd = getNumber('!') / this.TICKS_PER_DAY + this.TICKS_EPOCH;
							break;
						case '*':
							iValue = value.length;
							break;
						case '\'':
							if (doubled('\'')) {
								checkLiteral();
							}
							else {
								literal = true;
							}
							break;
						default:
							checkLiteral();
					}
				}
			}
			if (iValue < value.length) {
				throw $.calendars.local.unexpectedText || $.calendars.regionalOptions[''].unexpectedText;
			}
			if (year === -1) {
				year = this.today().year();
			}
			else if (year < 100 && shortYear) {
				year += (shortYearCutoff === -1 ? 1900 : this.today().year() -
					this.today().year() % 100 - (year <= shortYearCutoff ? 0 : 100));
			}
			if (doy > -1) {
				month = 1;
				day = doy;
				for (var dim = this.daysInMonth(year, month); day > dim; dim = this.daysInMonth(year, month)) {
					month++;
					day -= dim;
				}
			}
			return (jd > -1 ? this.fromJD(jd) : this.newDate(year, month, day));
		},

		/** A date may be specified as an exact value or a relative one.
			Found in the <code>jquery.calendars.plus.js</code> module.
			@memberof BaseCalendar
			@param {CDate|number|string} dateSpec The date as an object or string in the given format or
					an offset - numeric days from today, or string amounts and periods, e.g. '+1m +2w'.
			@param {CDate} defaultDate The date to use if no other supplied, may be <code>null</code>.
			@param {CDate} [currentDate=null] The current date as a possible basis for relative dates,
					if <code>null</code> today is used.
			@param {string} [dateFormat] The expected date format -
					see {@linkcode BaseCalendar.formatDate|formatDate}. Use '' for the calendar default format.
			@param {object} [settings] Additional options whose attributes include:
			@param {number} [settings.shortYearCutoff] The cutoff year for determining the century.
			@param {string[]} [settings.dayNamesShort] Abbreviated names of the days from day 0 (Sunday).
			@param {string[]} [settings.dayNames] Names of the days from day 0 (Sunday).
			@param {string[]} [settings.monthNamesShort] Abbreviated names of the months.
			@param {string[]} [settings.monthNames] Names of the months.
			@return {CDate} The decoded date. */
		determineDate: function(dateSpec, defaultDate, currentDate, dateFormat, settings) {
			if (currentDate && typeof currentDate !== 'object') {
				settings = dateFormat;
				dateFormat = currentDate;
				currentDate = null;
			}
			if (typeof dateFormat !== 'string') {
				settings = dateFormat;
				dateFormat = '';
			}
			var calendar = this;
			var offsetString = function(offset) {
				try {
					return calendar.parseDate(dateFormat, offset, settings);
				}
				catch (e) {
					// Ignore
				}
				offset = offset.toLowerCase();
				var date = (offset.match(/^c/) && currentDate ?
					currentDate.newDate() : null) || calendar.today();
				var pattern = /([+-]?[0-9]+)\s*(d|w|m|y)?/g;
				var matches = pattern.exec(offset);
				while (matches) {
					date.add(parseInt(matches[1], 10), matches[2] || 'd');
					matches = pattern.exec(offset);
				}
				return date;
			};
			defaultDate = (defaultDate ? defaultDate.newDate() : null);
			dateSpec = (typeof dateSpec === 'undefined' || dateSpec === null ? defaultDate :
				(typeof dateSpec === 'string' ? offsetString(dateSpec) : (typeof dateSpec === 'number' ?
				(isNaN(dateSpec) || dateSpec === Infinity || dateSpec === -Infinity ? defaultDate :
				calendar.today().add(dateSpec, 'd')) : calendar.newDate(dateSpec))));
			return dateSpec;
		}
	});

})(jQuery);

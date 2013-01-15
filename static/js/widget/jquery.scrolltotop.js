/**
 * escrolltotop jquery�ص����������ƽ�����ض�����
 * 
 * ��������
 *   startline : ���ַ��ض�����ť�붥���ľ���
 *   scrollto : ���������붥���ľ��룬����ĳ��idԪ�ص�λ��
 *   scrollduration : ƽ������ʱ��
 *   fadeduration : ���뵭��ʱ�� eg:[ 500, 100 ] [0]���롢[1]����
 *   controlHTML : html����
 *   className ����ʽ����
 *   titleName : �ص�������title����
 *   offsetx : �ص����� right ƫ��λ��
 *   offsety : �ص����� bottom ƫ��λ��
 *   anchorkeyword : è������
 * eg:
 *   $.scrolltotop({
 *   	scrollduration: 1000 
 *   });
 */
(function($){
	$.scrolltotop = function(options){
		options = jQuery.extend({
			startline : 100,				//���ַ��ض�����ť�붥���ľ���
			scrollto : 0,					//���������붥���ľ��룬����ĳ��idԪ�ص�λ��
			scrollduration : 500,			//ƽ������ʱ��
			fadeduration : [ 500, 100 ],	//���뵭��ʱ�� ��[0]���롢[1]����
			controlHTML : '<a href="javascript:;"><b>�ص�������</b></a>',		//html����
			className: '',					//��ʽ����
			titleName: '�ص�����',				//�ص�������title����
			offsetx : 5,					//�ص����� right ƫ��λ��
			offsety : 5,					//�ص����� bottom ƫ��λ��
			anchorkeyword : '#top', 		//è������
		}, options);
		
		var state = {
			isvisible : false,
			shouldvisible : false
		};
		
		var current = this;
		
		var $body,$control,$cssfixedsupport;
		
		var init = function(){
			var iebrws = document.all;
			$cssfixedsupport = !iebrws || iebrws
					&& document.compatMode == "CSS1Compat"
					&& window.XMLHttpRequest
			$body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
			$control = $('<div class="'+options.className+'" id="topcontrol">' + options.controlHTML + '</div>').css({
				position : $cssfixedsupport ? 'fixed': 'absolute',
				bottom : options.offsety,
				right : options.offsetx,
				opacity : 0,
				cursor : 'pointer'
			}).attr({
				title : options.titleName
			}).click(function() {
				scrollup();
				return false;
			}).appendTo('body');
			if (document.all && !window.XMLHttpRequest && $control.text() != ''){
				$control.css({
					width : $control.width()
				});
			}
			togglecontrol();
			$('a[href="' + options.anchorkeyword + '"]').click(function() {
				scrollup();
				return false;
			});
			$(window).bind('scroll resize', function(e) {
				togglecontrol();
			})
			
			return current;
		};
		
		var scrollup = function() {
			if (!$cssfixedsupport){
				$control.css( {
					opacity : 0
				});
			}
			var dest = isNaN(options.scrollto) ? parseInt(options.scrollto): options.scrollto;
			if(typeof dest == "string"){
				dest = jQuery('#' + dest).length >= 1 ? jQuery('#' + dest).offset().top : 0;
			}
			$body.animate( {
				scrollTop : dest
			}, options.scrollduration);
		};

		var keepfixed = function() {
			var $window = jQuery(window);
			var controlx = $window.scrollLeft() + $window.width()
					- $control.width() - options.offsetx;
			var controly = $window.scrollTop() + $window.height()
					- $control.height() - options.offsety;
			$control.css( {
				left : controlx + 'px',
				top : controly + 'px'
			});
		};

		var togglecontrol = function() {
			var scrolltop = jQuery(window).scrollTop();
			if (!$cssfixedsupport){
				this.keepfixed()
			}
			state.shouldvisible = (scrolltop >= options.startline) ? true : false;
			if (state.shouldvisible && !state.isvisible) {
				$control.stop().animate( {
					opacity : 1
				}, options.fadeduration[0]);
				state.isvisible = true;
			} else if (state.shouldvisible == false && state.isvisible) {
				$control.stop().animate( {
					opacity : 0
				}, options.fadeduration[1]);
				state.isvisible = false;
			}
		};
		
		return init();
	};
})(jQuery);
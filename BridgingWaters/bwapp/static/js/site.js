;$(document).ready(function(){

	$('#showHideAdvanced').toggle(function() {
		$('#advancedSearchDiv').slideDown(400);
		$('#showHideAdvanced span').html('Hide Advanced Options');
		$('#search1').hide();
		$('#search2').show();
	}, function() {
		$('#advancedSearchDiv').slideUp(200);
		$('#showHideAdvanced span').html('Show Advanced Options');
		$('#search1').show();
		$('#search2').hide();
	});
	
	
	$('#showHideMap').toggle(function() {
		$('#mapDiv').slideUp(200);
		$('#showHideMap').html('Show Map');
		
	}, function() {
		$('#mapDiv').slideDown(400);
		$('#showHideMap').html('Hide Map');
	});
	
	$('a.trunc_show').toggle(function() {
	    $(this).siblings('span.trunc').hide();
	    $(this).siblings('span.untrunc').show();
	    $(this).html('Less');
	    $(this).attr('title','View Less');
	}, function() {
	    $(this).siblings('span.untrunc').hide();
	    $(this).siblings('span.trunc').show();
	    $(this).html('More');
	    $(this).attr('title','View More');
	});
	
	// Menu
	$('#topMenu li').css({backgroundPosition: '50% -20px'}).hover(function() {
			$(this).stop().animate({backgroundPosition:"50% -10px"}, {duration:200});
		},function() {
			$(this).stop().animate({backgroundPosition :"50% -20px"}, {duration:200});
		}
	);
		
	$('a.ajax-link').click( function( event ) {
		set_ajax_link( $(this), event );
	});
		
	
	$( "#login_form" ).dialog({
		autoOpen: false,
		height: 300,
		width: 350,
		modal: true,
		resizable: false,
		buttons: {
			"Submit": function() {
				$( this ).dialog( "close" );
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			
		}
	});
	
	$( "#login_link" ).click(function() {
		$( "#login_form" ).dialog( "open" );
		return false;
	});


});

function set_ajax_link( el, event ){
	event.preventDefault();
	var url = el.attr("href");
	load_page_content( url, el );
}
function load_page_content( url, el ){
	$("#ajaxContent").load( url + ' #main', { 'ajax': 'true' }, 
		function(){
			$('.sub_nav li.active').removeClass('active');
			$(el).parent().addClass('active');
		});
}

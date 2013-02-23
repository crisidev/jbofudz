$(function() {
	// Setup uploader
	$("#uploader").pluploadQueue({
		// General settings
		runtimes : 'html5,flash,html4',
		url : 'upload',
		max_file_size : '1000mb',
		chunk_size : '1000mb',
		unique_names : true,
		file_data_name : 'upfile',

		// Resize images on clientside if we can
		resize : {width : 320, height : 240, quality : 90},
		// Flash settings
		flash_swf_url : 'static/js/plupload.flash.swf'
	});
});

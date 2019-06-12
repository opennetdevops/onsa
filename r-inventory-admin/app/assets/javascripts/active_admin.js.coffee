#= require active_admin/base
#= require activeadmin_addons/all

$ ->
  $('#access_node_device_model_id').change ->
	  if $('#select2-access_node_device_model_id-container').attr('title') != ""
	  	id = $('#access_node_device_model_id option:selected').val()
	  	console.log($('#access_node_device_model_id option:selected').val())
	  	$.ajax "/device_models/" + id + "/" + "uplink_ports",
		    type: 'GET'
		    dataType: 'json'
		    success: (data, textStatus, jqXHR) ->
		        $('select[id="access_node_uplink_ports"]').empty()
		        $.each data, (index,element) ->
			        $('select[id="access_node_uplink_ports"]').append('<option value=' + element + '>' + element + '</option>');

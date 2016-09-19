// this function makes an AJAX call to run oncofuse_results
// and check the database.  A JSON object is returned will all the data
function oncofuse_results(  ) {
	// hide parts that aren't populated and set up the loader gif
  $('#fusion_ids').empty();
	$('#result_count').empty();
	$("#run_oncofuse").prop("disabled",true);
	$('#submit_column').hide();
  $('#loader').show();
	$('#results').hide();
	$('#oncofuse_report').hide();
	$('#literature_report').hide();
	$('#empty_lit_report').hide();
	$('#empty_onco_report').hide();
  var user_input = $('#user_input').serialize();
	var fd = new FormData();
  var file_data = $('#input_file')[0].files[0];
  fd.append('input_file', file_data);

	$.ajax({
		url: "../chimera_quest/view.py?" + user_input,
		data: fd,
		type: "POST",
		dataType: "json",
		processData: false,
		contentType: false,
		success: function(results, textStatus, jqXHR) {
      console.log("success")
			if(results.length < 1) {
        console.log("no results found")
				$('#result_count').text( "0" );
				$('#oncofuse_report').hide();
				$('#literature_report').hide();
				$('#empty_onco_report').show();
			} else {
      console.log("results found")
				$('#result_count').text( results.length );
			    $.each( results, function( i, value ) {
					object_string = JSON.stringify(value);
					var result_button = "<li class='button'><input name='fusion' type='radio' value='" + object_string + "'>" + value.id + "</li>"
					$( "#fusion_ids" ).append(result_button);
				})
			}
			$('#loader').hide();
			$('#submit_column').show();
			$('#results').show();
			$("#run_oncofuse").prop("disabled",false);
		},
		error: function(jqXHR, textStatus, errorThrown){
			console.log("fail")
			alert("Failed to perform fusion gene search! textStatus: (" + textStatus +
				  ") and errorThrown: (" + errorThrown + ")");
			$('#loader').hide();
			$('#submit_column').show();
			$('#results').hide();
			$("#run_oncofuse").prop("disabled",false);
		}
	})
};

// this function parses the data from oncofuse and populates the report
function make_oncofuse_report(  ){
	console.log("oncofuse report")
	var fusions = $('#fusion').serializeArray();
	var fusion = $.parseJSON(fusions[0].value)
		$('#report_header').text( fusion.id );
		$('#driver_probability').text( fusion.driver_probability );
		$('#fusion_coordinates').text( fusion.fusion_coordinates );
		$('#passenger_probability').text( fusion.passenger_probability );
		$('#expression_gain').text( fusion.expression_gain );
		$('#spanning_reads').text( fusion.spanning_reads );
		$('#encompassing_reads').text( fusion.encompassing_reads );
		$('#frame_difference').text( fusion.frame_difference );
		$('#five_partner').text( fusion.five_partner );
		$('#five_breakpoint_summary').text( fusion.five_breakpoint_summary );
		$('#five_gene_length').text( fusion.five_gene_length );
		$('#five_domains_retained').text( fusion.five_domains_retained );
		$('#five_pathways_retained').text( fusion.five_pathways_retained );
		$('#five_interaction_interfaces').text( fusion.five_interaction_interfaces );
		$('#five_domains_broken').text( fusion.five_domains_broken );
		$('#three_partner').text( fusion.three_partner );
		$('#three_breakpoint_summary').text( fusion.three_breakpoint_summary );
		$('#three_gene_length').text( fusion.three_gene_length );
		$('#three_domains_retained').text( fusion.three_domains_retained );
		$('#three_pathways_retained').text( fusion.three_pathways_retained );
		$('#three_interaction_interfaces').text( fusion.three_interaction_interfaces );
		$('#three_domains_broken').text( fusion.three_domains_broken );
		$('#literature_report').hide();
		$('#oncofuse_report').show();
		$('#empty_lit_report').hide();
		$('#empty_onco_report').hide();
};

// this function parses the data from the literature database
// and populates the report
function make_literature_report(  ){
	console.log("lit report")
	var fusions = $('#fusion').serializeArray();
	var fusion = $.parseJSON(fusions[0].value)
	// this if loop will show a special no-results report
	if (fusion.total_matches < 1 || fusion.total_matches == null) {
		$('#empty_lit_header').text( fusion.id );
		$('#oncofuse_report').hide();
		$('#literature_report').hide();
		$('#empty_lit_report').show();
	} else {
  	$('#lit_report_header').text( fusion.id );
  	$('#total_matches').text( fusion.total_matches );
  	$('#pubmed_matches').text( fusion.pubmed_matches );
  	$('#pubmed_diseases').text( fusion.pubmed_diseases );
  	$('#pubmed_references').text( fusion.pubmed_references );
  	$('#omim_matches').text( fusion.omim_matches );
  	$('#omim_diseases').text( fusion.omim_diseases );
  	$('#omim_references').text( fusion.omim_references );
  	$('#omim_annotation').text( fusion.omim_annotation );
  	$('#sanger_matches').text( fusion.sanger_matches );
  	$('#sangercgp_diseases').text( fusion.sangercgp_diseases );
  	$('#sangercgp_head_gene_locus').text( fusion.sangercgp_head_gene_locus );
  	$('#sangercgp_head_gene_function').text( fusion.sangercgp_head_gene_function );
  	$('#sangercgp_tail_gene_locus').text( fusion.sangercgp_tail_gene_locus );
  	$('#sangercgp_tail_gene_function').text( fusion.sangercgp_tail_gene_function );
  	$('#mitelman_matches').text( fusion.mitelman_matches );
  	$('#mitelman_diseases').text( fusion.mitelman_diseases );
  	$('#mitelman_abnormality').text( fusion.mitelman_abnormality );
  	$('#mitelman_fusion_locus').text( fusion.mitelman_fusion_locus );
  	$('#mitelman_head_gene_locus').text( fusion.mitelman_head_gene_locus );
  	$('#mitelman_tail_gene_locus').text( fusion.mitelman_tail_gene_locus );
  	$('#oncofuse_report').hide();
  	$('#literature_report').show();
  	$('#empty_lit_report').hide();
  	$('#empty_onco_report').hide();
	}
};

// run our javascript once the page is ready
$(document).ready( function() {
  $('#help').hide();
  $('#loader').hide();
  $('#results').hide();
	$('#help').hide();
  $('#downloads').hide();
  $('#user_input').submit( function() {
      oncofuse_results();
      return false;
	});
	$('#onco_report').click( function() {
		make_oncofuse_report();
		return false;
	});
	$('#lit_report').click( function() {
		make_literature_report();
		return false;
	});
	$('#help_button').click( function() {
	    $('#help').show();
	    $('.home').hide();
	    $('#downloads').hide();
		return false;
	});
	$('#sample_files').click( function() {
		$('#help').hide();
		$('.home').hide();
		$('#downloads').show();
		return false;
	});
	$('#home_button').click( function() {
		$('#help').hide();
		$('.home').show();
	    $('#results').hide();
	    $('#downloads').hide();
		return false;
	});
});

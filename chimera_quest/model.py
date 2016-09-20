
"""

This script consists of three functions, run_oncofuse() will take the user input and run oncofuse, output_parser() will parse the oncofuse output and literature_search() will search for each fusion identified in the literature database. Oncofuse also creates a dictionary of results for each fusion, which is then converted to a JSON object to return.

"""

import json
import os
import mysql.connector
import subprocess
from random import choice
from string import ascii_uppercase


# this function will take the input and run oncofuse
def run_oncofuse( user_input ):
	tissue_type, input_type, input_file = user_input
	input_file_name = ''.join(choice(ascii_uppercase) for i in range(15)) + ".txt"
	input_file_path = os.path.join("./static/tmp", input_file_name )
	user_file = open(input_file_path, "w")
	user_file.write(input_file)
	user_file.close()


	output_file_name = ''.join(choice(ascii_uppercase) for i in range(15)) + ".txt"
	output_file_path = os.path.join("./static/oncofuse_outputs", output_file_name)


	# Store the command to run oncofuse as a string
	command = "java -Xmx1G -jar ./oncofuse/Oncofuse.jar {} {} {} {}".format(input_file_path, input_type, tissue_type, output_file_path )
	command = command.split()

	# Run oncofuse and open/read the results
	subprocess.call( command )

	# store results in a list

	results = open(output_file_path).readlines()
	# for line in open(output_file_path).readlines():
	# 	results = results + line
	# delete any files created
	deleter = "rm {} {}".format(input_file_path, output_file_path)
	deleter = deleter.split()
	subprocess.call(deleter)

	return(results)

# this function will search the literature database
# and a dictionary of the matches
def literature_search( id ):

	# connect to the biosql database
	conn = mysql.connector.connect( user=os.environ['user'], password=os.environ['password'],
										host=os.environ['host'], db=os.environ['db'] )
	curs = conn.cursor()

	# lists to hold info from databases
	pubmed_diseases = []
	pubmed_references = []
	omim_diseases = []
	omim_references = []
	omim_annotation = []
	sangercgp_diseases = []
	sangercgp_head_gene_locus = []
	sangercgp_head_gene_function = []
	sangercgp_tail_gene_locus = []
	sangercgp_tail_gene_function = []
	mitelman_diseases = []
	mitelman_abnormality = []
	mitelman_fusion_locus = []
	mitelman_head_gene_locus = []
	mitelman_tail_gene_locus = []
	pubmed_matches = 0
	omim_matches = 0
	sanger_matches = 0
	mitelman_matches = 0

	################################## pubmed stuff
	# query for matchcount and diseases
	qry = """
	select bioentry.description
	from bioentry
	where bioentry.name = %s
	and bioentry.accession like "PubMed:%";
	"""

	# execute the select statement
	curs.execute( qry, ( id, ) )

	for d in curs:
		diseases = d[0].split("+")
		pubmed_diseases.extend(diseases)
		pubmed_matches += 1


	qry = """
	select dbxref.dbname, dbxref.accession
	from dbxref
	join bioentry_dbxref on bioentry_dbxref.dbxref_id=dbxref.dbxref_id
	join bioentry on bioentry.bioentry_id=bioentry_dbxref.bioentry_id
	where bioentry.name = %s
	and bioentry.accession like "PubMed:%";
	"""
	# execute the select statement
	curs.execute( qry, ( id, ) )

	for db, a in curs:
		acc = a.decode("utf-8")
		pubmed_references.append(acc)

	###################################### OMIM stuff
	# get diseases and match count
	qry = """
	select bioentry.description
	from bioentry
	where bioentry.name = %s
	and bioentry.accession like "OMIM:%";
	"""

	curs.execute( qry, ( id, ) )

	for d in curs:
		diseases = d[0]
		omim_diseases.append(diseases)
		omim_matches += 1

	# get database references
	qry = """
	select dbxref.dbname, dbxref.accession
	from dbxref
	join bioentry_dbxref on bioentry_dbxref.dbxref_id=dbxref.dbxref_id
	join bioentry on bioentry.bioentry_id=bioentry_dbxref.bioentry_id
	where bioentry.name = %s
	and bioentry.accession like "OMIM:%";
	"""

	curs.execute( qry, ( id, ) )

	for db, a in curs:
		db = db.decode("utf-8")
		acc = a.decode("utf-8")
		if len(acc) > 0:
			db_acc = "{}:{}".format(db, acc)
			omim_references.append(db_acc)

	# get omim title
	qry = """
	select term.name, bioentry_qualifier_value.value
	from term
	join bioentry_qualifier_value on bioentry_qualifier_value.term_id=term.term_id
	join bioentry on bioentry.bioentry_id=bioentry_qualifier_value.bioentry_id
	where bioentry.name = %s
	and bioentry.accession like "OMIM:%";
	"""

	curs.execute( qry, ( id, ) )

	for t, value in curs:
		term = t.decode("utf-8")
		if term == "omim_title" and len(value) > 0:
			omim_annotation.append(value)

	###################################### sanger stuff
	# get diseases and match count
	qry = """
	select bioentry.description
	from bioentry
	where bioentry.name = %s
	and bioentry.accession like "SangerCGP:%";
	"""

	curs.execute( qry, ( id, ) )

	for d in curs:
		diseases = d[0].split("+")
		sangercgp_diseases.extend(diseases)
		sanger_matches += 1

	# get head and tail gene info
	qry = """
	select term.name, bioentry_qualifier_value.value
	from term
	join bioentry_qualifier_value on bioentry_qualifier_value.term_id=term.term_id
	join bioentry on bioentry.bioentry_id=bioentry_qualifier_value.bioentry_id
	where bioentry.name = %s
	and bioentry.accession like "SangerCGP:%";
	"""

	curs.execute( qry, ( id, ) )

	for t, value in curs:
		term = t.decode("utf-8")
		if term == "head_gene_locus" and len(value) > 0:
			sangercgp_head_gene_locus.append(value)
		if term == "head_gene_function" and len(value) > 0:
			sangercgp_head_gene_function.append(value)
		if term == "tail_gene_locus" and len(value) > 0:
			sangercgp_tail_gene_locus.append(value)
		if term == "tail_gene_function" and len(value) > 0:
			sangercgp_tail_gene_function.append(value)



	###################################### sanger stuff
	# get diseases and match count
	qry = """
	select bioentry.description
	from bioentry
	where bioentry.name = %s
	and bioentry.accession like "Mitelman:%";
	"""

	curs.execute( qry, ( id, ) )

	for d in curs:
		diseases = d[0].split("+")
		mitelman_diseases.extend(diseases)
		mitelman_matches += 1

	# get head and tail gene info
	qry = """
	select term.name, bioentry_qualifier_value.value
	from term
	join bioentry_qualifier_value on bioentry_qualifier_value.term_id=term.term_id
	join bioentry on bioentry.bioentry_id=bioentry_qualifier_value.bioentry_id
	where bioentry.name = %s
	and bioentry.accession like "Mitelman:%";
	"""

	curs.execute( qry, ( id, ) )

	for t, value in curs:
		term = t.decode("utf-8")
		if term == "head_gene_locus" and len(value) > 0:
			mitelman_head_gene_locus.append(value)
		if term == "tail_gene_locus" and len(value) > 0:
			mitelman_tail_gene_locus.append(value)
		if term == "abnormality" and len(value) > 0:
			mitelman_abnormality.append(value)
		if term == "fusion_locus" and len(value) > 0:
			mitelman_fusion_locus.append(value)

	# close database connection
	curs.close()
	conn.close()

	# Turn all lists into strings
	if len(pubmed_diseases) > 0:
		pubmed_diseases = ", ".join(set(pubmed_diseases))
	else: pubmed_diseases = "None reported"
	if len(pubmed_references) > 0:
		pubmed_references = ", ".join(set(pubmed_references))
	else: pubmed_references = "None reported"
	if len(omim_diseases) > 0:
		omim_diseases = ", ".join(set(omim_diseases))
	else: omim_diseases = "None reported"
	if len(omim_references) > 0:
		omim_references = ", ".join(set(omim_references))
	else: omim_references = "None reported"
	if len(omim_annotation) > 0:
		omim_annotation = ", ".join(set(omim_annotation))
	else: omim_annotation = "None reported"
	if len(sangercgp_diseases) > 0:
		sangercgp_diseases = ", ".join(set(sangercgp_diseases))
	else: sangercgp_diseases = "None reported"
	if len(sangercgp_head_gene_locus) > 0:
		sangercgp_head_gene_locus = ", ".join(set(sangercgp_head_gene_locus))
	else: sangercgp_head_gene_locus = "None reported"
	if len(sangercgp_head_gene_function) > 0:
		sangercgp_head_gene_function = ", ".join(set(sangercgp_head_gene_function))
	else: sangercgp_head_gene_function = "None reported"
	if len(sangercgp_tail_gene_locus) > 0:
		sangercgp_tail_gene_locus = ", ".join(set(sangercgp_tail_gene_locus))
	else: sangercgp_tail_gene_locus = "None reported"
	if len(sangercgp_tail_gene_function) > 0:
		sangercgp_tail_gene_function = ", ".join(set(sangercgp_tail_gene_function))
	else: sangercgp_tail_gene_function = "None reported"
	if len(mitelman_diseases) > 0:
		mitelman_diseases = ", ".join(set(mitelman_diseases))
	else: mitelman_diseases = "None reported"
	if len(mitelman_abnormality) > 0:
		mitelman_abnormality = ", ".join(set(mitelman_abnormality))
	else: mitelman_abnormality = "None reported"
	if len(mitelman_fusion_locus) > 0:
		mitelman_fusion_locus = ", ".join(set(mitelman_fusion_locus))
	else: mitelman_fusion_locus = "None reported"
	if len(mitelman_head_gene_locus) > 0:
		mitelman_head_gene_locus = ", ".join(set(mitelman_head_gene_locus))
	else: mitelman_head_gene_locus = "None reported"
	if len(mitelman_tail_gene_locus) > 0:
		mitelman_tail_gene_locus = ", ".join(set(mitelman_tail_gene_locus))
	else: mitelman_tail_gene_locus = "None reported"


	# get the sum of all matches
	total_matches = pubmed_matches + omim_matches + sanger_matches + mitelman_matches

	literature_results = {
		"total_matches" : total_matches,
		"pubmed_matches" : pubmed_matches,
		"pubmed_diseases" : pubmed_diseases,
		"pubmed_references" : pubmed_references,
		"omim_matches" : omim_matches,
		"omim_diseases" : omim_diseases,
		"omim_references" : omim_references,
		"omim_annotation" : omim_annotation,
		"sanger_matches" : sanger_matches,
		"sangercgp_diseases" : sangercgp_diseases,
		"sangercgp_head_gene_locus" : sangercgp_head_gene_locus,
		"sangercgp_head_gene_function" : sangercgp_head_gene_function,
		"sangercgp_tail_gene_locus" : sangercgp_tail_gene_locus,
		"sangercgp_tail_gene_function" : sangercgp_tail_gene_function,
		"mitelman_matches" : mitelman_matches,
		"mitelman_diseases" : mitelman_diseases,
		"mitelman_abnormality" : mitelman_abnormality,
		"mitelman_fusion_locus" : mitelman_fusion_locus,
		"mitelman_head_gene_locus" : mitelman_head_gene_locus,
		"mitelman_tail_gene_locus" : mitelman_tail_gene_locus,
	}
	return(literature_results)

def chimera_quest( user_input ):
	results = run_oncofuse( user_input )
	num = 0
	fusion_list = []
	for line in results:
		num += 1
		# skip header line and gather data
		data = line.split('\t')
		if num > 1 and len(data) == 36:
			# general data about the fusion
			fusion_coordinates = data[5]
			driver_probability = data[22]
			passenger_probability = data[21]
			expression_gain = data[23]
			spanning_reads = data[3]
			encompassing_reads = data[4]
			frame_difference = data[20]
			# data about the head gene
			five_cds = data[7]
			five_segment_type = data[8].lower()
			five_segment_number = data[9]
			five_breakpoint = data[10]
			five_frame = data[12]
			five_gene_length = data[11]
			five_partner = data[6]
			five_interaction_interfaces = data[28]
			five_domains_retained = data[24]
			five_domains_broken = data[26]
			five_pathways_retained = data[28]

			# data about the tail gene
			three_cds = data[14]
			three_segment_type = data[15].lower()
			three_segment_number = data[16]
			three_breakpoint = data[17]
			three_frame = data[19]
			three_gene_length = data[18]
			three_partner = data[13]
			three_interaction_interfaces = data[28]
			three_domains_retained = data[25]
			three_domains_broken = data[27]
			three_pathways_retained = data[29]

			# clean up the data for presentation
			id = "{}:{}".format(five_partner, three_partner)

			# search the literature database
			literature_results = literature_search( id )

			# make a summary statement about the breakponts
			if five_cds == "Yes": five_cds = "was"
			if five_cds == "No": five_cds = "was not"
			if three_cds == "Yes": three_cds = "was"
			if three_cds == "No": three_cds = "was not"

			five_breakpoint_summary = "The head gene (five-prime partner) {} cleaved at a CDS.  The breakpoint was in {} number {} at residue number {} of that segment and was translated in frame {} (frame 0 is in-frame).".format(five_cds, five_segment_type, five_segment_number, five_breakpoint, five_frame)

			three_breakpoint_summary = "The tail gene (three-prime partner) {} cleaved at a CDS.  The breakpoint was in {} number {} at residue number {} of that segment and was translated in frame {} (frame 0 is in-frame).".format(three_cds, three_segment_type, three_segment_number, three_breakpoint, three_frame)

			# check for empty variables
			if len(five_interaction_interfaces) < 1:
				five_interaction_interfaces = "None reported"
			if len(five_domains_retained) < 1:
				five_domains_retained = "None reported"
			if len(five_domains_broken) < 1:
				five_domains_broken = "None reported"
			if len(five_pathways_retained) < 1:
				five_pathways_retained = "None reported"
			if len(three_interaction_interfaces) < 1:
				three_interaction_interfaces = "None reported"
			if len(three_domains_retained) < 1:
				three_domains_retained = "None reported"
			if len(three_domains_broken) < 1:
				three_domains_broken = "None reported"
			if len(three_pathways_retained) < 1:
				three_pathways_retained = "None reported"

			# create a fusion object for each result
			result = {
				"id":id,
				"fusion_coordinates":fusion_coordinates,
				"driver_probability":driver_probability,
				"passenger_probability":passenger_probability,
				"expression_gain":expression_gain,
				"spanning_reads":spanning_reads,
				"encompassing_reads":encompassing_reads,
				"frame_difference":frame_difference,
				"five_partner":five_partner,
				"three_partner":three_partner,
				"five_breakpoint_summary":five_breakpoint_summary,
				"three_breakpoint_summary":three_breakpoint_summary,
				"five_gene_length":five_gene_length,
				"five_interaction_interfaces":five_interaction_interfaces,
				"five_domains_retained":five_domains_retained,
				"five_domains_broken":five_domains_broken,
				"five_pathways_retained":five_pathways_retained,
				"three_gene_length":three_gene_length,
				"three_interaction_interfaces":three_interaction_interfaces,
				"three_domains_retained":three_domains_retained,
				"three_domains_broken":three_domains_broken,
				"three_pathways_retained":three_pathways_retained,
					}
			result.update(literature_results)
			fusion_list.append(result)

			# clear all variables
			result, data, fusion_coordinates, driver_probability, passenger_probability, expression_gain, spanning_reads, encompassing_reads, frame_difference, five_cds, five_segment_type, five_segment_number, five_segment_position, five_frame, five_gene_length, five_partner, five_interaction_interfaces, five_domains_retained, five_domains_broken, five_pathways_retained, three_cds, three_segment_type, three_segment_number, three_segment_position, three_frame, three_gene_length, three_partner, three_interaction_interfaces, three_domains_retained, three_domains_broken, three_pathways_retained, id, five_summary, three_summary = {}, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None


	return(json.dumps(fusion_list, separators=(",",":")))

if __name__ == '__main__':
    chimera_quest( user_input )

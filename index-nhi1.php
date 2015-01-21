`f<?php

	require_once("_ifapi/src/isdk.php");

	extract($_GET);
	if (empty( $contact_id )==true)  extract($_POST);

	$app = new iSDK;

	$results      = array();
	$comparason   = array();

               # these 4 digit numbers correspond to tag id for answer to each assessment question in Infusionsoft form
	$questionaire = array( "tinnutis" =>array ("y" => array(1796, 1826, 1856, 1886),
	                                                                               "n" => array(1800, 1830, 1860, 1890),
		                                                                "s" => array(1798, 1828, 1858, 1888)
				),

				"hearing" =>array("y" => array(1808, 1838, 1868, 1898 ),
	                                                                                "n" => array(1812, 1842, 1872, 1902),
						       "s" => array(1810, 1840, 1870, 1900)
				),

				"hyperacusis" =>array("y" => array(1802, 1832, 1862, 1892),
	                                                                                         "n" => array(1806, 1836, 1866, 1896),
							 "s" => array(1804, 1834, 1864, 1894)
				),

				"dizziness" => array("y" => array(1814, 1844, 1874, 1904),
	                                                                                    "n" => array(1818, 1848, 1878, 1908),
						           "s" => array(1816, 1846, 1876, 1906)
				),

				"blockear"    => array("y" => array(1820, 1850, 1880, 1910 ),
	                                                                                      "n" => array(1824, 1854, 1884, 1914),
						             "s" => array(1822, 1852, 1882, 1912)
				),

	);

	$tag_result = array( "tinnutis" => 2278, "hyperacusis" => 2280, "hearing" => 2282, "dizziness" => 2284, "blockear" => 2286 );


	function query_tags($contact_id) {

		global $app;

		$returnFields = array('GroupId');
		$query = array('ContactId' => $contact_id );
		$tags = $app->dsQuery("ContactGroupAssign",100,0,$query,$returnFields);

		foreach ( $tags as $a =>$b ) $retval[]=$b['GroupId'];

		return $retval;

	}

	function get_results($tag_id){

		global $questionaire;
		global $results;

		foreach( $questionaire as $a => $b ) {
			foreach( $b as $c =>$d ) {
				foreach( $d as $e ) {
					if ( $e == $tag_id ) {

						$results[ $a ][ $c ][ 'count' ] += 1;
						$results[ $a ][ $c ][ 'tags' ][] = $e;

						if ( $c == 'y' ) $results[ $a ][ 'scores' ] += 5;
						elseif ( $c == 's' ) $results[ $a ][ 'scores' ] += 3;

						$results[ $a ][ 'qtags' ][] = strval( $e );
					}
				}
			}
		}
	}

	if ($app->cfgCon("youraccountname")) {

		$contact_tags = query_tags($contact_id);

		foreach( $contact_tags as $ctag_id) {
			get_results($ctag_id);
		}

		if ($_GET[ override ] == true ) {
			$results[ tinnutis ][ scores ]=$_GET[ tinnutis ];
			$results[ hearing ][ scores ]=$_GET[ hearing ];
			$results[ dizziness ][ scores ]=$_GET[ dizziness ];
			$results[ hyperacusis ][ scores ]=$_GET[ hyperacusis ];
			$results[ blockear ][ scores ]=$_GET[ blockear ];
		}

		foreach( $results as $cat => $val ) {
			$comparason[$cat] = $val[ scores ];
			echo 'Category '.$cat.' scores '.$val[ scores ].'<br>';
		}

		$highest_score = max( $comparason );

	}

	echo '<br>The major score is => '.$highest_score;

	foreach( $comparason as $a => $b ) {
		if ($b==$highest_score) {
			if (empty($final_result)==true) $final_result = $a;
		}
	}

	echo '<br>Final Result => '.$final_result;
	echo '<br>Tag Final Result '.$tag_result[$final_result];

	echo '<br><br>Raw Referrence Data : <br> <pre>';
	print_r( $results );

	$data = array(	'_AssessmentType'  => "nameofyourassessment",
			'_AssessmentOption0' => ucfirst($final_result),
			'_AssessmentScore' => $highest_score,
			'_AssessmentScoreCondition1'=> $results[ tinnutis ][ scores ],
			'_AssessmentScoreCondition2'=> $results[ hearing ][ scores ],
			'_AssessmentScoreCondition3'=> $results[ dizziness ][ scores ],
			'_AssessmentScoreCondition4'=> $results[ hyperacusis ][ scores ],
			'_AssessmentScoreCondition5'=> $results[ blockear ][ scores ]);

	$app->updateCon($contact_id, $data);
	$app->grpAssign($contact_id, $tag_result[$final_result]);

	print_r( $data );

	echo '<br>contact id '.$contact_id;
	echo '<br>tag id result '.$tag_result[$final_result];

?>
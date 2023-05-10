<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:xs="http://www.w3.org/2001/XMLSchema" 
	xmlns:math="http://exslt.org/math" 
	xmlns:functx="http://www.functx.com" 
	xmlns:common="http://common" 
	xmlns:saxon="http://saxon.sf.net/"
	xmlns:exslt="http://exslt.org/common" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	extension-element-prefixes="saxon" 
	exclude-result-prefixes="exslt saxon common" version="2.0">
	<xsl:output method="xml" encoding="UTF-8" indent="yes"/> <!-- output is a text file -->
	<xsl:variable name="interfaceCount"  saxon:assignable="yes" select="0"/> <!-- works as a global variable -->
	<xsl:variable name="api_judge_value"  saxon:assignable="yes" select="0"/>
	<xsl:template match="/">
		<ROOT>
			<xsl:for-each select="//SDD">
				<xsl:variable name="listOfApiFunction"><!-- create a list that contains all the name of the api_function -->
					<LIST>
						<xsl:for-each select=".//memberdef[@kind = 'function']">
							<xsl:if test="ancestor::compounddef[@id = 'group___l_i_s_t___o_f___p_u_b_l_i_c___i_n_t_e_r_f_a_c_e_s']"><!-- search the all the parentnodes in certain condition -->
								<xsl:element name="FUNCTION">
									<xsl:attribute name="Name" select="./name"/>
								</xsl:element>
							</xsl:if>
						</xsl:for-each>
					</LIST>
				</xsl:variable>
				<xsl:element name="SWC">
					<xsl:for-each select="descendant::para"><!-- search all the childnodes with nodename para -->
						<xsl:variable name="ref_value">
							<xsl:value-of select="."/>
						</xsl:variable>
						<xsl:if test="contains($ref_value,'Component Name')"><!-- if the value of node para contains 'Component Name' -->
							<xsl:for-each select="following::para[position()=1]"><!-- search all the nodes after this node with name para and pick the first one -->
								<xsl:variable name="name_value">
									<xsl:value-of select="translate(.,' ','')"/><!-- replace the space with '',that means delete the space -->
								</xsl:variable>
								<xsl:attribute name="Name" select="$name_value"/>
							</xsl:for-each>
						</xsl:if>
					</xsl:for-each>
					<xsl:variable name="localSwcNode" select="."/><!-- create a node point -->
					<xsl:for-each select="distinct-values(.//memberdef[@kind = 'function']/name)"><!-- search all the required nodes with different name and loop the name -->
						<xsl:variable name="functionName" select="."/>
						<xsl:variable name="localFunctionIsApi" select="count($listOfApiFunction//FUNCTION[@Name = $functionName]) &gt;0"/><!-- judge if this name of function is api_function -->
						<xsl:for-each select="($localSwcNode//memberdef[@kind = 'function' and ./name = $functionName and not(starts-with($functionName, 'TEST_'))])[1]">
							<xsl:element name="FUNCTION" >
								<xsl:attribute name="Name" select="./name"/>
								<xsl:attribute name="Api" select="if($localFunctionIsApi = true()) then 'Yes' else 'No'"/>
								<xsl:for-each select="./param">
									<xsl:element name="PARAM" >
										<xsl:if test="exists(./declname)">
											<xsl:attribute name="Name" select="./declname"/>
										</xsl:if>
										<xsl:attribute name="DataType" select="./type"/>
									</xsl:element>
								</xsl:for-each>
								<xsl:element name="RETURN" >
									<xsl:attribute name="DataType" select="./type"/>
								</xsl:element>
							</xsl:element>
						</xsl:for-each>
					</xsl:for-each>
				</xsl:element>
			</xsl:for-each>
		</ROOT>
	</xsl:template>
	
	<xsl:variable name="root" select="/"/>      <!-- this is the "root" node of the tree -->
	<xsl:variable name="EOL" select="'&#xA;'"/> <!-- CR in ASCII -->
	<xsl:variable name="TAB" select="'&#x9;'"/> <!-- tab in ASCII -->
</xsl:stylesheet><!--Tabsymbol'&#x9;'-->

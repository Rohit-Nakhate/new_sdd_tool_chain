@echo off
rem -------------------------------------------------------------------------------
rem -[CONFIG AREA]-----------------------------------------------------------------
set ts_mirr_path=%TS_LOCAL%
set JAVA=%ts_mirr_path%\xml\jre1.5.0\bin\java.exe -Duser.language=en -Xmx256m
set JAVA6=%ts_mirr_path%\xml\jre6u45\bin\java.exe -Duser.language=en -Xmx256m
set XALANPATH=-Djava.endorsed.dirs="%ts_mirr_path%\xml\xerces2.6.2;%ts_mirr_path%\xml\xalan2.6.0;;%ts_mirr_path%\xml\saxon-b"
set XINCLUDE=-Dorg.apache.xerces.xni.parser.XMLParserConfiguration=org.apache.xerces.parsers.XIncludeParserConfiguration
set XALAN=net.sf.saxon.Transform
set VALIDATE=net.sf.saxon.Validate

set PROJECT_VARIANT=Evo
set XMLPRJ_PATH=temp\%PROJECT_VARIANT%\_SDD_ICAS%PROJECT_VARIANT%.xmlprj

echo -[gen]--------------------------------------------------------------------
IF EXIST .\temp\%PROJECT_VARIANT% (
	rd /s /q temp\%PROJECT_VARIANT%
)
mkdir .\temp\%PROJECT_VARIANT%
py python/merge.bat.py ..\..\.. merge%PROJECT_VARIANT%.bat %PROJECT_VARIANT%
py python/mk.xmlprj.py ..\..\.. %XMLPRJ_PATH% %PROJECT_VARIANT%
call merge%PROJECT_VARIANT%.bat
%JAVA% %XALANPATH% %XINCLUDE% %XALAN% -s:%XMLPRJ_PATH% -xsl:xsl\export.xml.xsl  -o:out\SDD_ICAS%PROJECT_VARIANT%.xml
if not defined DEBUG (
	rd /s /q temp
	del /f /q merge%PROJECT_VARIANT%.bat
	)
echo -[DONE]-------------------------------------------------------------------


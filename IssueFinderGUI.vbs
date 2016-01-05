Function HubbleGUI
    Dim logPath
    blnValid = False
    
    ' Create an IE object
    Set objIE = CreateObject( "InternetExplorer.Application" )
    ' specify some of the IE window's settings
    objIE.Navigate "about:blank"
    objIE.Document.Title = "IssueFinder"
    objIE.ToolBar        = False
    objIE.Resizable      = False
    objIE.StatusBar      = False
    objIE.Width          = 800
    objIE.Height         = 510
    ' Center the dialog window on the screen
    'With objIE.Document.ParentWindow.Screen
    '    objIE.Left = (.AvailWidth  - objIE.Width ) \ 2
    '    objIE.Top  = (.Availheight - objIE.Height) \ 2
    'End With
    ' Wait till IE is ready
    Do While objIE.Busy
        WScript.Sleep 200
    Loop
    
    ' Insert the HTML code to prompt for user input
    objIE.Document.Body.InnerHTML = "<DIV ALIGN=""CENTER"">" _
              & "<TABLE CELLSPACING=""5"">" _
              & "<TR NOWRAP><TH COLSPAN=""2"" STYLE=""font-size:1.5em"">" _
              & "IssueFinder Parameters" _
              & "</TH></TR>" _
              & "<TR NOWRAP><TH COLSPAN=""2"" STYLE=""BORDER-BOTTOM: 1px solid #CFCFCF;color:red"">" _
              & "* Make sure PC is logged into Qualnet before running<br>" _
              & "* Multiple paths should be separated by comma, like path1,path2,...)" _
              & "</TH></TR>" _
              & "<TR NOWRAP><TD VALIGN=""TOP"">Log Path:</TD>" _
              & "<TD><TEXTAREA STYLE=""width:450px;height:130px;"" " _
              & "ID=""logPath""></TEXTAREA></TD></TR>" _
              & "</TABLE>" _
              & "<P><INPUT TYPE=""hidden"" ID=""OK"" " _
              & "NAME=""OK"" VALUE=""0"">" _
              & "<INPUT TYPE=""submit"" VALUE="" OK "" " _
              & "OnClick=""VBScript:OK.Value=1"" STYLE=""WIDTH:100px;""></P><P STYLE=""font:normal 0.75em Arial;color:#CFCFCF"">Powered by PDT.CHINA.TDA</P></DIV>"
    ' Make the window visible
    objIE.Visible = True
    
    ' Wait for valid input (2 non-empty equal passwords)
    Do Until blnValid = True
        ' Wait till the OK button has been clicked
        On Error Resume Next
        Do While objIE.Document.All.OK.Value = 0
            WScript.Sleep 200
            If Err Then
                HubbleGUI = ""
                objIE.Quit
                Set objIE = Nothing
                Exit Function
            End If
        Loop
        On Error Goto 0
        ' Read the user input from the dialog window
        param = objIE.Document.All.logPath.Value
        ' Check if the new password and confirmed password match
        If param = "" Then
            MsgBox "Log path cannot be empty", _
                   vbOKOnly + vbInformation + vbApplicationModal, _
                   "Please input log path!"
            objIE.Document.All.OK.Value              = 0
        Else
            blnValid = True
        End If
    Loop
    ' Close and release the object
    objIE.Quit
    Set objIE = Nothing
    ' Return the passwords in an array
    HubbleGUI = param
End Function

param = HubbleGUI
If param <> "" Then
    Set wss=createobject("wscript.shell")
    wss.run "IssueFinder.bat """& param &""""
End If
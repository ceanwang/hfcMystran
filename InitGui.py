
class hfcMystranWorkbench (Workbench):
    "hfcMystran workbench object"
    Icon = """
        /* XPM */
        static char * Surface_Tools_Workbench_Main_xpm[] = {
        "16 16 48 1",
        " 	c None",
        ".	c #171D96",
        "+	c #1A229B",
        "@	c #222CA1",
        "#	c #181D95",
        "$	c #232DA2",
        "%	c #3344B3",
        "&	c #2A36A9",
        "*	c #181C96",
        "=	c #181B94",
        "-	c #161C96",
        ";	c #4961C8",
        ">	c #5776D5",
        ",	c #192098",
        "'	c #171C96",
        ")	c #394DB9",
        "!	c #5C7DDB",
        "~	c #5B7BDA",
        "{	c #465FC5",
        "]	c #384AB5",
        "^	c #4D67CB",
        "/	c #4D67CC",
        "(	c #171D97",
        "_	c #3D51BC",
        ":	c #181E96",
        "<	c #181E97",
        "[	c #4961C7",
        "}	c #1B2099",
        "|	c #1F269E",
        "1	c #506DCF",
        "2	c #516ED0",
        "3	c #171F96",
        "4	c #4861C8",
        "5	c #5A7BDA",
        "6	c #2631A5",
        "7	c #191E97",
        "8	c #181F99",
        "9	c #1B229A",
        "0	c #445AC3",
        "a	c #597AD9",
        "b	c #1F279E",
        "c	c #2E3BAD",
        "d	c #181D97",
        "e	c #192097",
        "f	c #181D98",
        "g	c #181F97",
        "h	c #3C51BC",
        "i	c #10128F",
        "                ",
        "                ",
        "          ..    ",
        "          +@    ",
        "  #$%&*= -;>,   ",
        " ')!!!~{]^!!/(  ",
        " '!!!!!!!!!!!_: ",
        " <[!!!!!!!!!!!} ",
        "  |!!!!11!!!!23 ",
        "  :4!567890!ab  ",
        "   |!c    def   ",
        "   gh(          ",
        "    i           ",
        "                ",
        "                ",
        "                "};
        """
    MenuText = "hfcMystran"
    ToolTip = "This is hfcMystran workbench"
	
    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
	
        import hfcMystranDatInFem
        self.appendToolbar("Pre", ["hfcMystranDatInFem"])
		
        import hfcMystranDatInFemWire
        self.appendToolbar("Pre", ["hfcMystranDatInFemWire"])
		
        import hfcMystranOpenDat
        self.appendToolbar("Pre", ["hfcMystranOpenDat"])
		
        import hfcMystranRun
        self.appendToolbar("Solve", ["hfcMystranRun"])
		
        import hfcMystranLogIn
        self.appendToolbar("Solve", ["hfcMystranLogIn"])

        import hfcMystranErrIn
        self.appendToolbar("Solve", ["hfcMystranErrIn"])

        import hfcMystranNeuIn
        self.appendToolbar("Post", ["hfcMystranNeuIn"])
		
        import hfcMystranNeuInWire
        self.appendToolbar("Post", ["hfcMystranNeuInWire"])
		
        import hfcMystranF06In
        self.appendToolbar("Post", ["hfcMystranF06In"])
		
        Log("Loading hfcMystran... done\n")

    def Activated(self):
        # do something here if needed...
        Msg("hfcMystran.Activated()\n")

    def Deactivated(self):
        # do something here if needed...
        Msg("hfcMystran.Deactivated()\n")

FreeCADGui.addWorkbench(hfcMystranWorkbench)
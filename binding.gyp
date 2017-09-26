{
 "variables": {
  "stable": "../../../stable/",
  "ext": "node",
  "prefix": "",
 },
 "conditions": [
  [
   "OS=='win'",
   {
    "variables": {
     "epeios": "<!(IF DEFINED EPEIOS_SRC (echo <(stable)) ELSE (echo src/epeios/))",
     "src": "<!(IF DEFINED EPEIOS_SRC (echo ./) ELSE (echo src/) )",
     "ext": "dll",
     "prefix": "",
    },
   },
   {
    "variables": {
     "epeios": "<!(if [ \"$EPEIOS_SRC\" != \"\" ]; then echo <(stable); else echo src/epeios/; fi)",
     "src": "<!(if [ \"$EPEIOS_SRC\" != \"\" ]; then echo ./; else echo src/; fi)",
      "conditions": [
      [
       "OS=='linux'",
       {
	    "ext": "so",
	    "prefix": "lib",
       },
      ],
      [
       "OS=='mac'",
       {
	    "ext": "dylib",
	    "prefix": "lib",
       }
      ],
     ],
    },
   }
  ]
 ],
 "targets": [
  {
   "target_name": "<(module_name)",
   "type": "shared_library",
   "sources": [ "<(src)/rncqnjs.cpp", "<(src)/registry.cpp", "<(epeios)/ags.cpp", "<(epeios)/aem.cpp", "<(epeios)/bch.cpp", "<(epeios)/bitbch.cpp", "<(epeios)/bso.cpp", "<(epeios)/cio.cpp", "<(epeios)/cpe.cpp", "<(epeios)/crptgr.cpp", "<(epeios)/cslio.cpp", "<(epeios)/crt.cpp", "<(epeios)/ctn.cpp", "<(epeios)/dir.cpp", "<(epeios)/dte.cpp", "<(epeios)/dtfbsc.cpp", "<(epeios)/dtfptb.cpp", "<(epeios)/epsmsc.cpp", "<(epeios)/err.cpp", "<(epeios)/fdr.cpp", "<(epeios)/flf.cpp", "<(epeios)/flsq.cpp", "<(epeios)/flw.cpp", "<(epeios)/flx.cpp", "<(epeios)/ias.cpp", "<(epeios)/idsq.cpp", "<(epeios)/iof.cpp", "<(epeios)/iop.cpp", "<(epeios)/lck.cpp", "<(epeios)/lst.cpp", "<(epeios)/lstbch.cpp", "<(epeios)/lstcrt.cpp", "<(epeios)/lstctn.cpp", "<(epeios)/mns.cpp", "<(epeios)/mtk.cpp", "<(epeios)/mtx.cpp", "<(epeios)/ntvstr.cpp", "<(epeios)/que.cpp", "<(epeios)/sdr.cpp", "<(epeios)/stkbse.cpp", "<(epeios)/stkbch.cpp", "<(epeios)/stkctn.cpp", "<(epeios)/str.cpp", "<(epeios)/strng.cpp", "<(epeios)/tagsbs.cpp", "<(epeios)/tol.cpp", "<(epeios)/txf.cpp", "<(epeios)/tys.cpp", "<(epeios)/uys.cpp", "<(epeios)/utf.cpp", "<(epeios)/xtf.cpp", "<(epeios)/llio.cpp", "<(epeios)/dlbrry.cpp", "<(epeios)/n4all.cpp", "<(epeios)/n4njs.cpp", "<(epeios)/plgn.cpp", "<(epeios)/plgncore.cpp", "<(epeios)/tht.cpp", "<(epeios)/thtsub.cpp", "<(epeios)/uvqdcl.cpp", "<(epeios)/bomhdl.cpp", "<(epeios)/cdgb64.cpp", "<(epeios)/fil.cpp", "<(epeios)/fnm.cpp", "<(epeios)/lcl.cpp", "<(epeios)/mthitg.cpp", "<(epeios)/mthrtn.cpp", "<(epeios)/stkcrt.cpp", "<(epeios)/rgstry.cpp", "<(epeios)/stsfsm.cpp", "<(epeios)/xml.cpp", "<(epeios)/xpp.cpp", "<(epeios)/sclargmnt.cpp", "<(epeios)/sclmisc.cpp", "<(epeios)/sclerror.cpp", "<(epeios)/scllocale.cpp", "<(epeios)/sclrgstry.cpp", "<(epeios)/scln4a.cpp", "<(epeios)/sclnjs.cpp", "<(src)/rncalg.cpp", "<(src)/rnccmn.cpp", "<(src)/rncflt.cpp", "<(src)/rncrpn.cpp", "<(src)/rncrtn.cpp", 
],
    "defines": ["VERSION=\"20170926\"", "COPYRIGHT_YEARS=\"2017\""],
   "include_dirs":  [ "<(src)", "<(epeios)", ],
   "conditions": [
    [
     "OS=='win'",
     {
      "sources": ["<(epeios)/wllio.cpp", ],
      "msvs_settings": {
       "VCCLCompilerTool": {
        "RuntimeLibrary": 0,
        "ExceptionHandling": 1,
        "MultiProcessorCompilation": "Yes",
        "AdditionalOptions": [ "/EHsc", ]
       },
       "VCLinkerTool": {
       },
       "VCLibrarianTool": {
       },
      },
     },
     {
      "sources": ["<(epeios)/pllio.cpp",       ],
      "cflags_cc": ["-std=gnu++11", "-fexceptions"],
     }
    ],
    [
     "OS=='mac'",
     {
      "defines": ["MTX_NATIVE", "MTX_SUPPRESS_WARNING"],
      "xcode_settings": { "GCC_ENABLE_CPP_EXCEPTIONS": "YES" },
     }
    ],
   ],
  },
  {
   "target_name": "action_after_build",
   "dependencies": [ "<(module_name)" ],
   "type": "none",
   "copies": [
    {
     "files": [ "<(PRODUCT_DIR)/<(module_name).<(ext)" ],
     "destination": "<(module_path)"
    }
   ]
  }
 ],
}
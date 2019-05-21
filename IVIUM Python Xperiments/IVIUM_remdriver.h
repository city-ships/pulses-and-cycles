// example header file for importing the IVIUM drivers in C++ Builder
// first add the IVIUM_remdriver.lib to the project
// if necessary it can be generated from the dll with the implib tool:
//             IMPLIB.EXE IVIUM_remdriver.lib IVIUM_remdriver.dll


#define IVIUM_API long __stdcall
#ifdef __cplusplus


extern "C" {
#endif
IVIUM_API   IV_open();
IVIUM_API   IV_close();
IVIUM_API   IV_selectdevice(long *devnr);
IVIUM_API   IV_getdevicestatus(long *devstatus);
IVIUM_API   IV_readSN(char *sntext);
IVIUM_API   IV_connect(long* devconnect);
IVIUM_API   IV_getcellstatus(long *devcellstatus);

IVIUM_API   IV_setcellon(long *cellon);
IVIUM_API   IV_setconnectionmode(long *value);
IVIUM_API   IV_setcurrentrange(long *value);
IVIUM_API   IV_setpotential(double *value);
IVIUM_API   IV_getpotential(double *value);
IVIUM_API   IV_getcurrent(double *value);
IVIUM_API   IV_setcurrent(double *value);

IVIUM_API   IV_setpotentialWE2(double *value);
IVIUM_API   IV_getcurrentWE2(double *value);
IVIUM_API   IV_setcurrentrangeWE2(double *value);
IVIUM_API   IV_setbistatmode(double *value);

IVIUM_API   IV_setfrequency(double *value);
IVIUM_API   IV_setamplitude(double *value);
IVIUM_API   IIV_setfilter(long *value);
IVIUM_API   IV_setstability(long *value);

IVIUM_API   IV_setdac(long *channr, double *value);
IVIUM_API   IV_getadc(long *channr, double *value);
IVIUM_API   IV_setmuxchannel(long *value);
IVIUM_API   IV_setdigout(long *value);
IVIUM_API   IV_getdigin(long *value);

IVIUM_API   IV_readmethod(char* fname);
IVIUM_API   IV_savemethod(char *fname);
IVIUM_API   IV_setmethodparameter(char *parname, char *parvalue);
IVIUM_API   IV_startmethod(char *fname);
IVIUM_API   IV_savedata(char *fname);
IVIUM_API   IV_getdata(long *pointnr,double *x, double *y, double *z);
IVIUM_API   IV_Ndatapoints(long *value);

IVIUM_API   IV_getcurrenttrace(long* npoints,double *rate,double *values);
IVIUM_API   IV_getpotentialtrace(long* npoints, double *rate,double *values);
IVIUM_API   IV_getcurrentWE2trace(long* npoints,double *rate,double *values);

IVIUM_API   IV_we32setoffset(long* index,double *value);
IVIUM_API   IV_we32setchannel(long* index);
IVIUM_API   IV_we32setoffsets(long* channels,double *values);
IVIUM_API   IV_we32getoffsets(long* channels,double *values);
IVIUM_API   IV_we32readcurrents(double *values);


#ifdef __cplusplus
}
#endif





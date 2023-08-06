/**************************************************************************

  Procedural intervace to the methods of Lipschitz interpolant classes
 ***************************************************************************/

//#ifdef __cplusplus
//extern "C" {
//#endif


//#define NULL 0
#define LIBEXP extern

/* interface to the members of SLipInt class ===================== */
LIBEXP double	LipIntValue(int* Dim, int* Ndata, double* x, double* Xd,double* y,  double* Lipconst, int* Index);
LIBEXP double	LipIntValueAuto(int* Dim, int* Ndata, double* x,double* Xd, double* y, int* Index);
LIBEXP double	LipIntValueCons(int* Dim, int* Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, int* Index);
LIBEXP double	LipIntValueConsLeftRegion(int* Dim, int* Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index);
LIBEXP double	LipIntValueConsRightRegion(int* Dim, int* Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index);
LIBEXP double	LipIntValueLocal(int *Dim, int *Ndata, double* x, double* Xd,double* y);
LIBEXP double	LipIntValueLocalCons(int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y);
LIBEXP double	LipIntValueLocalConsLeftRegion(int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region);
LIBEXP double	LipIntValueLocalConsRightRegion(int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region);
LIBEXP  void	LipIntComputeLipschitz(int *Dim, int *Ndata, double* x, double* y);
LIBEXP  void 	LipIntComputeLocalLipschitz(int *Dim, int *Ndata, double* x, double* y);
LIBEXP  void	LipIntComputeLipschitzCV(int *Dim, int *Ndata, double* Xd, double* y, double* T, int* type, int* Cons, double* Region, double *W);
LIBEXP  void	LipIntComputeLipschitzSplit(int *Dim, int *Ndata, double* Xd, double* y, double* T, double* ratio,int* type, int* Cons, double* Region, double *W);
LIBEXP void	LipIntSmoothLipschitz(int *Dim, int *Ndata,  double* Xd, double* y, double* T,  double* LC, int* fW, int* fC, int* fR, double* W, int* Cons, double* Region);
 // fR is 0, 1-left, 2-right
LIBEXP double	LipIntGetLipConst() ;
LIBEXP void		LipIntGetScaling(double *S) ;
LIBEXP int		LipIntComputeScaling(int *Dim, int *Ndata, double* XData, double* YData);
LIBEXP void	ConvertXData(int *Dim, int* npts,  double* XData);
LIBEXP void	ConvertXDataAUX(int *Dim, int* npts,  double* XData, double *auxdata);
LIBEXP int		LipIntVerifyMonotonicity(int *Dim, int* npts, int* Cons,  double* XData, double* YData, double* LC, double* eps);
LIBEXP int		LipIntVerifyMonotonicityLeftRegion(int *Dim, int* npts, int* Cons,  double* XData, double* YData, double* Region, double* LC, double* eps);
LIBEXP int		LipIntVerifyMonotonicityRightRegion(int *Dim, int* npts, int* Cons,  double* XData, double* YData, double* Region, double* LC, double* eps);
/* interface to the members of SLipIntInf class ====================================== */
LIBEXP double	LipIntInfValue(int *Dim, int *Ndata, double* x, double* Xd,double* y,  double* Lipconst, int* Index);
LIBEXP double	LipIntInfValueAuto(int *Dim, int *Ndata, double* x,double* Xd, double* y, int* Index);
LIBEXP double	LipIntInfValueCons(int *Dim, int *Ndata, int* Cons, double* x, double* Xd,double* y,  double Lipconst, int* Index);
LIBEXP double	LipIntInfValueConsLeftRegion(int *Dim, int *Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index);
LIBEXP double	LipIntInfValueConsRightRegion(int *Dim, int *Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index);
LIBEXP double	LipIntInfValueLocal(int *Dim, int *Ndata, double* x, double* Xd,double* y);
LIBEXP double	LipIntInfValueLocalCons(int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y);
LIBEXP double	LipIntInfValueLocalConsLeftRegion(int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region);
LIBEXP double	LipIntInfValueLocalConsRightRegion(int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region);
LIBEXP void	LipIntInfComputeLipschitz(int *Dim, int *Ndata, double* x, double* y);
LIBEXP void	LipIntInfComputeLocalLipschitz(int *Dim, int *Ndata, double* x, double* y);
LIBEXP void	LipIntInfComputeLipschitzCV(int *Dim, int *Ndata, double* Xd, double* y, double* T, int* type, int* Cons, double* Region, double *W);
LIBEXP void	LipIntInfComputeLipschitzSplit(int *Dim, int *Ndata, double* Xd, double* y, double* T, double* ratio, int* type, int* Cons, double* Region, double *W);
LIBEXP void	LipIntInfSmoothLipschitz(int *Dim, int *Ndata,  double* Xd, double* y, double* T,  double* LC,  int* fW, int* fC, int* fR, double* W, int* Cons, double* Region);
 // fR is 0, 1-left, 2-right
LIBEXP double	LipIntInfGetLipConst() ;
LIBEXP void	LipIntInfGetScaling(double *S) ;
LIBEXP int		LipIntInfComputeScaling(int *Dim, int *Ndata, double* XData, double* YData);
LIBEXP int		LipIntInfVerifyMonotonicity(int *Dim, int* npts, int* Cons,  double* XData, double* YData, double LC, double ep);
LIBEXP int		LipIntInfVerifyMonotonicityLeftRegion(int *Dim, int npts, int* Cons,  double* XData, double* YData, double* Region, double* LC, double* eps);
LIBEXP int		LipIntInfVerifyMonotonicityRightRegion(int *Dim, int npts, int* Cons,  double* XData, double* YData, double* Region, double* LC, double* eps);
LIBEXP void	LipIntInfSmoothLipschitzSimp(int *Dim, int* npts,  double* XData, double* YData, double* TData,  double* LC);
LIBEXP void	LipIntInfSmoothLipschitzSimpW(int *Dim, int* npts,  double* XData, double* YData, double* TData,  double* LC, double* W);
/* interface to the members of STCInterpolant class ====================================== */
// supplies the data to Interpolant and constructs the interpolant
// assuming a given Lipschitz constant, supplied by SetLipschitz
// if LipConstant was not supplied, tries to find it from the data
// assumes that all data are different. 
LIBEXP int	STCBuildLipInterpolant(int *Dim, int *Ndata, double* x, double* y);
// as above, but for explicit evaluation, needs no preprocessing, but may be slower
LIBEXP int	STCBuildLipInterpolantExplicit(int *Dim, int *Ndata, double* x, double* y);
// in the methods above, the coordinates of the data points in x are stored in rows
// the following methods store data in columns (like in fortran or Matlab)
// they use the transposed of the matrix x 
LIBEXP  int	STCBuildLipInterpolantColumn(int *Dim, int *Ndata, double* x, double* y);
// as above, but for explicit evaluation, needs no preprocessing, but may be slower
LIBEXP  int	STCBuildLipInterpolantExplicitColumn(int *Dim, int *Ndata, double* x, double* y);
// specify the Lipschitz constant for your function
LIBEXP void	STCSetLipschitz(double* x);
// computes the value of the interpolant at any given point x
LIBEXP  double	STCValue( double* x );
// same but using explicit evaluation with no preprocessing
LIBEXP  double	STCValueExplicit( double* x );
LIBEXP void	STCFreeMemory();
// additional functions
LIBEXP void LipIntConstruct( int id);
LIBEXP double LipIntDetermineLipschitz( int id);
LIBEXP void LipIntFreeMemory( int id);
LIBEXP void LipIntSetConstants( int id);
LIBEXP double LipIntValueExplicitDim( int id, int dim, double* x);
LIBEXP double LipIntValueDim( int id, int dim, double* x);
LIBEXP void LipIntSetData( int id, int dim, int K, double* x, double* y, int test);
LIBEXP int	STCInterpolantInit();
LIBEXP void	STCInterpolantDel( int id);
LIBEXP int SLipIntInit();
LIBEXP void SlipIntDel( int id);
LIBEXP int SLipIntInfInit();
LIBEXP void SLipIntInfDel( int id);
LIBEXP int SLipIntLpInit();
LIBEXP void SLipIntLpDel( int id);
// #ifdef __cplusplus
// }
// #endif

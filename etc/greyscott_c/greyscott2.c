#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define oekaki
/*
#define moji 
*/
#ifdef oekaki
#include <GLUT/glut.h>
#endif
extern double drand48(void);
extern void srand48(long seedval);

int height = 800, width = 400;
int height2 = 1;

#define N 800
#define NT 800
int itime=0;
int TIME=  1000;
double  yy[N][NT];
double  zz[N][NT];
int    Nsize=800;
/*  how many times to iterate before visualizing */
int Niter=20;
double   color[N];
static double F = 0.018; 
static double K1 = 0.077;
static double K2 = 0.36; 
static double K3 = 0.004;
static double diffU = .2;
static double diffV = .1;
static double diffW = 0.02;

double u[N],v[N],w[N];
double du[N],dv[N],dw[N];
double u2[N],v2[N],w2[N];

void dynA(double *u,double *v,double *w,int i)
{

int p = i ;
int left  = (i+width-1)%width;
int right = (i+1)%width;

double uvv = u[p]*v[p]*v[p];
double vww = v[p]*w[p]*w[p];
double lapU = ( u[left] + u[right] - 2*u[p] );
double lapV = ( v[left] + v[right] - 2*v[p] );
double lapW = ( w[left] + w[right] - 2*w[p] );
           

            du[p] = diffU * lapU - uvv + F*(1-u[p]);
            dv[p] = diffV * lapV + uvv - (F+K1)*v[p];
            dw[p]=0;
            /*
            dv[p] = diffV * lapV + uvv - K1*v[p] - K2*vww;
            dw[p] = diffW * lapW + K2*vww - K3*(w[p]);
            */
}
/*---------------------------------------
   main dynamics controling module 


   ----------------------------*/
void dynamics(void){
      double t;
      int i,j;
  double lll,rrr,ddd;
  int itime2=0;
  int iit=0;

itime++;
     itime2 = (itime)%height2; 
/*
   printf("%d  %d\n",itime,itime2);
*/
     while(iit<Niter){
    for(i=0;i<Nsize;i++){
         dynA(u,v,w,i);
    }
    for(i=0;i<Nsize;i++){
      u[i] += du[i] ;
      v[i] += dv[i];
      w[i] += dw[i];
    }
    for(i=0;i<Nsize;i++){
    if (u[i] <= 0)
      u[i]=0;
    if (v[i] <= 0)
      v[i]=0;
    if (w[i] <= 0)
      w[i]=0;
    }

    iit++;
    }

if(itime2 == 0){
  /*
   printf("++++++++++++++++ %d  %d\n",itime,itime2);
   */
   for(j=0;j<(height-1);j++){
    for(i=0;i<Nsize;i++){
    yy[i][j] = yy[i][j+1];
    zz[i][j] = zz[i][j+1];
    }
    }
    for(i=0;i<Nsize;i++){
    yy[i][height-1] = u[i];
    zz[i][height-1] = v[i];
    }
               }


}
void billiard(void){
  int i,j;
  int itime2;

#ifdef oekaki
  itime2 = (itime%height2);
  /*
printf("aaaaaaaaaaa %d \n",itime);
*/
  if(itime2==0){
  glBegin( GL_POINTS );
   for(j=0;j<height;j++){
  for(i=0;i<Nsize;i++){
      glPointSize(1);
   glColor3d(zz[i][j],0.4,yy[i][j]);
     glVertex2d(i,height-j);
      }
   }
glEnd();
glFlush();
   }
#endif
}
void display(void){
  int i; 
#ifdef oekaki
/*  glClearColor( 1, 0.9, 1, .0);
  glClear( GL_COLOR_BUFFER_BIT );
*/
#endif 
   billiard(); 
#ifdef oekaki
  glutSwapBuffers();
#endif
}

void idle(void){
  int time,k,i;
    dynamics();

  if(itime==TIME){
  exit(1);
  }
   
#ifdef oekaki
    if(itime>TIME){
    glutIdleFunc( NULL );
    }
      glutPostRedisplay(); 
#endif
}
int main(int argc, char** argv){
      int i,j,k;
      long int iseed;
      int nnnn;
      int nnnn2;
      int itime;
      int iflag;
	char filename[100];
     
      iseed = atoi(argv[1]);
      F = atof(argv[2]);
      K1 = atof(argv[3]);
      iflag = atoi(argv[4]);
      TIME = atoi(argv[5]);
      Nsize = atoi(argv[6]);

   for(itime=0;itime<height;itime++){
  for(i=0;i<Nsize;i++){
   yy[i][itime]=0;
   zz[i][itime]=0;
 }
   }
      srand48(iseed);

#ifdef oekaki
  glutInit( &argc, argv );
  glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB );
  glutInitWindowPosition( 10, 10 );
  glutInitWindowSize( width, height );
  glutCreateWindow( "GrayScott 1Dim" );
#endif

  if(iflag==0){
      for(i=0;i<Nsize;i++){
        u[i]=0.8*drand48();
        v[i]=0.4*drand48();
        w[i]=0;
  }
           }
  if(iflag==1){
      for(i=0;i<Nsize;i++)
	u[i] = 1;
	v[i] = 0;
	w[i] = 0;
	u[Nsize/2] = 0.5;
	v[Nsize/2] = 0.25;
	w[Nsize/2] = 0;
	u[Nsize/2-1] = 0.5;
	v[Nsize/2-1] = 0.25;
	w[Nsize/2-1] = 0;
	u[Nsize/2+1] = 0.5;
	v[Nsize/2+1] = 0.25;
	w[Nsize/2+1] = 0;
           }
  if(iflag==2){
      for(i=0;i<Nsize;i++){
	u[i] = 0;
	v[i] = 0;
	w[i] = 0;
   if(drand48()>0.5)
	u[i] = 1;
       }
           }

#ifdef moji
  itime=0;


  while(itime<TIME){
  itime++;
  idle();
}
#endif
#ifdef oekaki
  /* call-back */
  glutDisplayFunc( display );
  glutIdleFunc( idle );

  /* 2D-setup  */
  glMatrixMode( GL_PROJECTION );
  glLoadIdentity();
  gluOrtho2D( 0, width-1, 0., height-1);
  
  glutMainLoop();
#endif
 

  
  return 0;
}




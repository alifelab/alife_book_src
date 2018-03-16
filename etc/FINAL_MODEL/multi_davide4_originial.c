#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define oekaki
#undef GA
#ifdef oekaki
#include <GLUT/glut.h>
#endif
#define NNN 50  // number of agents
#define Nsize 16 // total number of neurons per agent
#define GAsize 20 // number of agents for GA operation
#define N  1000 // an arina : environment field (N mesh x N mesh)

extern double drand48(void);
extern void srand48(long seedval);
struct agent {
        int n;             // id
        double x,y,x2,y2; // coordinates
        double theta_base;  // heading
        double k; // kinetic energy
        double sigma[Nsize]; // neural state
};
static struct agent ant[NNN];

/*   total number of ants   */
int Nant;   // a total number of agents in the demonstration
/*   number of ants type2 < Nant */
int Nant2;  // different kinds of agents in the population
/*...................  parameters for neural netowrk .............*/
int Nsize1,Nsize2,Nsize3;   /* number of context and intermediate neurons  */
double gttt[Nsize][Nsize][GAsize];
double attt[Nsize][Nsize][GAsize];
double pheromone,rate_bgp;
double mutation_rate;
double param;
char filename[100],filename2[100];

/* ................... parameters for vehicle movement .......*/

int TIME=10000000;
int GTIME=1000;
int CircleLength;
int itime=0;
double vehicle_radius;
double theta;
double theta_vehicle;
double Vx,Vy;

/* ...................parameters for environmental structure ......*/

double bgp[N][N][GAsize];
int width = 200, height = 200;
double potential_radius=5;
int number_potential = 12;
double heat;
int xp[N],yp[N];

FILE *file[5];

/*---------------------- GetNN function:  get the weight vector from a data file */
void GetNN(char filename[],int m)
{
        int k,j;

        if(NULL==(file[m]=fopen(filename,"r")))
                printf("Failed To Open %s\n",filename);

        for(k=0; k<Nsize; k++) {
                for(j=0; j<Nsize; j++) {
                        fscanf(file[m],"%lf ",&attt[k][j][m]);
                        printf("%g ",attt[k][j][m]);
                }
                printf("\n");
        }
        printf("\n");
        fclose(file[m]);
}
/*...


 */
void navigation(int time,int m)
{
        double sum;
        int k,i,j,n;
        int intxx,intyy;
        double sigma2[Nsize];
        double xg,yg,theta_base;
        extern int dynamics();

        xg=ant[m].x;
        yg=ant[m].y;
        theta_base = ant[m].theta_base;

//   printf("%d %lf %lf ) ",m,xg,yg);
        for(k=1; k<Nsize3; k++) {
                intxx=(int)(xg+ vehicle_radius*cos(2.0*M_PI*k/(Nsize3-1)+theta_base));
                intyy=(int)(yg+ vehicle_radius*sin(2.0*M_PI*k/(Nsize3-1)+theta_base));

                if(intxx>(width-1))
                        intxx -= width;
                if(intxx<0)
                        intxx += width;
                if(intyy>(height-1))
                        intyy -= height;
                if(intyy<0)
                        intyy += height;

/*----  sensor input updated -----------------------------------*/
//    ant[m].sigma[k]= 1./(1.+exp(-bgp[intxx][intyy][1 - ant[m].n]));
                sum=0;
                for(j=0; j<Nant; j++) {
                        if(j != m) {
                                sum += bgp[intxx][intyy][j];
                        }
                }
                ant[m].sigma[k]= 1.0/(1.0+exp(-sum));

        }

        for(k=Nsize3; k<Nsize; k++) {
                sum=0;
                for(i=0; i<Nsize; i++) {
                        sum += ant[m].sigma[i]*gttt[k][i][ant[m].n];
                }
                sigma2[k] = 1/(1.+ exp(-sum));
        }

        for(k=Nsize3; k<Nsize; k++)
                ant[m].sigma[k] = sigma2[k];

/* navigation is computed */

        dynamics(Vx-ant[m].sigma[Nsize-2],Vy-ant[m].sigma[Nsize-1],m);

        itime++;
        if(itime%1000==-10)
                printf("******** %d %d %lf %lf %lf\n",itime,m,xg,yg,bgp[intxx][intyy][ant[m].n]);
}
/*.......................  to draw a circle .....*/
#ifdef oekaki

void circle(GLint res, GLdouble radius,double xxx,double yyy)
{
        int i;
        glBegin(GL_LINE_LOOP);
        glColor3d(0.9,0.9,0.2);
        for(i=0; i<res; i++)
                glVertex2d(xxx+radius*cos(2.0*M_PI*i/res),yyy+ radius*sin(2.0*M_PI*i/res));
        glEnd();
}
#endif
/* ...................... boundry check

   a periodic boundary is applied here and the agent has a finite body size.
   agents dwell in a torus environment.
   ...............................................*/
int Check_boundary(double x,double y)
{
        int sum = 0;

        if((x+vehicle_radius) > width)
                sum = 1;
        if((x-vehicle_radius) < 0)
                sum = 1;
        if((y+vehicle_radius) > height)
                sum += 2;
        if((y-vehicle_radius) < 0)
                sum += 2;
        return(sum);
}
void boundary(double *x1,double *y1){

        if(*x1<vehicle_radius)
                *x1 += 2*(vehicle_radius-*x1);

        if(*y1<vehicle_radius)
                *y1 += 2*(vehicle_radius-*y1);

        if(*x1>(height-vehicle_radius))
                *x1 += 2*(height-*x1-vehicle_radius);

        if(*y1>(height-vehicle_radius))
                *y1 += 2*(height-*y1-vehicle_radius);

}
double environment2(int xx,int yy){
        double dx,dy,dxy;
        double heat_effect=0.;
        int i;

        for(i=0; i<number_potential; i++) {

                dx = (double)xx - xp[i];
                dy = (double)yy - yp[i];

                dxy = sqrt(dx*dx + dy*dy);
                heat_effect += heat*exp(-dxy/potential_radius);
        }
        if(heat_effect>100)
                heat_effect=100;

        return(heat_effect);
}
/*------------------------------- bgp */
void init_bgp(void)
{
        int i,j,m;

        for(i=0; i<width; i++) {
                for(j=0; j<height; j++) {
                        for(m=0; m<Nant; m++) {
                                if(environment2(i,j)<0.02) {
                                        // bgp[i][j][m]=-pheromone/4.0;
                                        bgp[i][j][m]= 0;
                                }
                                else
                                        bgp[i][j][m] =  environment2(i,j);
                        }
                }
        }
}
#ifdef oekaki
/*-------------------------------plot  bgp */
void plot_bgp(void)
{
        int i,j,k;
        double bbb,bbb1,bbb2;
        int x1,y1;


        for(k=0; k<Nant; k++) {
                x1 = (int)(ant[k].x);
                y1 = (int)(ant[k].y);
                bgp[x1][y1][k] += pheromone;
        }

        glBegin( GL_POINTS );
        glPointSize(1);
        for(i=0; i<width; i++) {
                for(j=0; j<height; j++) {
                        bbb1=0;
                        for(k=0; k<Nant; k++) {
                                bgp[i][j][k] *= rate_bgp;
                                if(bgp[i][j][k]< 0.02) {
                                        bgp[i][j][k] = 0;
                                        bbb1 -= 0.1;
                                }else{
                                        bbb1 += bgp[i][j][k];
                                }
                        }
                        bbb2 = bbb1/Nant;
                        //bbb2 = 1.0/(1.+exp(-bbb1));
                        glColor3d(0.2,bbb2,0.9);
                        //glColor3d(0.2,0.5,0.9);
                        glVertex2d(i,j);
                }
        }
        glEnd();

}
#endif
/*---------------------------------------


   ----------------------------*/
int dynamics(double motor1,double motor2,int m){
        int icheck=0;
        double delta2=.1;
        int x1,y1;
        double delta_xg,delta_yg;
        double xg,yg,theta_base;

        theta_base = ant[m].theta_base;
        xg = ant[m].x;
        yg = ant[m].y;

        delta_xg = delta2*((motor1+motor2)*cos(theta_base));
        delta_yg = delta2*((motor1+motor2)*sin(theta_base));
        xg += delta_xg;
        yg += delta_yg;
        theta_base += 0.2*delta2*(motor1-motor2);

        if(xg>(width))
                xg -= width;
        if(yg>(height))
                yg -= height;
        if(xg<0)
                xg += height;
        if(yg<0)
                yg += height;

        ant[m].x = xg;
        ant[m].y = yg;
        ant[m].theta_base = theta_base;
        x1 = (int)(xg);
        y1 = (int)(yg);

        icheck = (int)bgp[x1][y1][ant[m].n];
        if( icheck < 0) { icheck=-1;}

        if(theta_base > 2*M_PI)
                theta_base -= 2*M_PI;
        if(theta_base < 0)
                theta_base += 2*M_PI;

        return(icheck);
}
#ifdef oekaki
void billiard2(void){
        int i,j,m;
        int itime2;
        double amp;
        double qqq;
        double xg,yg,theta_base;
        double ant_col;

        plot_bgp();
        amp = vehicle_radius;
        //         glColor3d(1.0,0.0,0.0);
        for(m=0; m<Nant; m++) {
                xg = ant[m].x;
                yg = ant[m].y;
                ant_col = ant[m].n;
                theta_base = ant[m].theta_base;

                circle(100,amp,xg,yg);
                glBegin(GL_LINE_LOOP);
                for(i=0; i<CircleLength; i++) {
                        glColor3d(1,ant_col,0.);
                        glVertex2d(xg+amp*cos(theta*i),yg+amp*sin(theta*i));
                }
                glVertex2d(xg,yg);
                glVertex2d(xg+2*amp*cos(theta_base),yg+2*amp*sin(theta_base));
                glVertex2d(xg,yg);
                glEnd();
        }
        glFlush();
}
/*.......................display ....*/
void display(void){
        int i,m;
        int itime2;
        double amp;

        glClear( GL_COLOR_BUFFER_BIT );

        if(itime%1==0) {
                glColor3d(0.3,0.8,0.1);

                billiard2();
                glutSwapBuffers();
        }
}
/*.......................idle ....*/
void idle(void){
        int time,m;
        double sumx,sumy;

        for(m=0; m<Nant; m++) {
                navigation(itime,m);
        }
        itime++;
        if(itime==TIME)
                exit(1);
        if(itime>TIME) {
                glutIdleFunc( NULL );
        }
        glutPostRedisplay();

}
#endif

int main(int argc, char** argv){
        int i,j,k,m;
        int yoko,tate;
        long int iseed;

/*---------  variables for NN ------*/
        int kk;
        int time_length=10;
        int time;
        int Iter=10;
        double dddd,rrr1;

        CircleLength = 100;
        number_potential = CircleLength;
        iseed = atoi(argv[1]);
        vehicle_radius =atoi(argv[2]);
        srand48(iseed);
        mutation_rate = atof(argv[3]);
        Nsize3 = atoi(argv[4]);
        Nsize1 = atoi(argv[5]);
        Nsize2 = Nsize-2;

        sprintf(filename,"%s",argv[6]);
        if(NULL==(file[0]=fopen(filename,"a")))
                printf("Failed To Open %s\n",filename);

        sprintf(filename2,"%s",argv[7]);
        if(NULL==(file[1]=fopen(filename2,"a")))
                printf("Failed To Open %s\n",filename);

        Nant2 = atoi(argv[8]);
        Vx=atof(argv[9]);
        Vy = Vx;
        heat = atof(argv[10]);
        potential_radius=atof(argv[11]);
        theta_vehicle= 2.0*M_PI/Nsize3;

        Nant = atoi(argv[12]);
        pheromone = atof(argv[13]);
        rate_bgp = atof(argv[14]);

/*.........................graphic charm  */
#ifdef oekaki
        glutInit( &argc, argv );
        glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB );
        glutInitWindowPosition( 10, 10 );
        glutInitWindowSize( width, height );
        glutCreateWindow( "DaisyWorld" );
#endif
/*---------------------  initialize network ----*/

        for(m=0; m<GAsize; m++) {
                for(k=0; k<Nsize; k++)
                        for(j=0; j<Nsize; j++)
                                gttt[j][k][m] = 1;

                for(j=Nsize3; j<(Nsize-2); j++) {
                        gttt[j][1][m] = (2.*drand48()-1.);
                }

                for(k=1; k<Nsize3; k++) {
                        for(j=Nsize3; j<Nsize1; j++) {
                                gttt[j][k][m] = (2.*drand48()-1.);
                        }
                }
                for(k=Nsize3; k<Nsize1; k++) {
                        for(j=Nsize1; j<Nsize; j++) {
                                gttt[j][k][m] = (2.*drand48()-1.);
                        }
                }
                for(k=Nsize1; k<(Nsize-2); k++) {
                        for(j=Nsize3; j<Nsize1; j++) {
                                gttt[j][k][m] = (2.*drand48()-1.);
                        }
                }
        }

//   initialize variables
        for(i=0; i<Nant; i++) {
                if(i<Nant2)
                        ant[i].n=0;
                else
                        ant[i].n=1;

                ant[i].x = (width-4*vehicle_radius)*drand48()+2*vehicle_radius;
                ant[i].y = (height-4*vehicle_radius)*drand48()+2*vehicle_radius;
                ant[i].x2=0;
                ant[i].y2=0;
                ant[i].k=0;
                for(j=0; j<Nsize; j++)
                        ant[i].sigma[j]=0.5;

                ant[i].sigma[0] = 1.;

                ant[i].theta_base = 0.5;
        }
/*...................... environment  ..............*/
        yoko=200;
        tate=200;
        theta= 4.0*M_PI/CircleLength;

        for(i=0; i<number_potential; i++) {
                rrr1 = (100+ 50*drand48());

                xp[i] = yoko+ (int)(rrr1*cos(theta*i));
                yp[i] = tate + (int)(rrr1*sin(theta*i));
        }

        init_bgp();
/*-----------------------  copy neural weights ....*/

#ifdef oekaki
        GetNN(filename,0);
        for(k=0; k<Nsize; k++) {
                for(j=0; j<Nsize; j++) {
                        gttt[k][j][0] = attt[k][j][0];
                        printf("%g ",gttt[k][j][0]);
                }
                printf("\n");
        }
        GetNN(filename2,1);
        for(k=0; k<Nsize; k++) {
                for(j=0; j<Nsize; j++) {
                        gttt[k][j][1] = attt[k][j][1];
                        printf("%g ",gttt[k][j][1]);
                }
                printf("\n");
        }
/*--------------------------------------------------------*/

        glutDisplayFunc( display );
        glutIdleFunc( idle );

        glMatrixMode( GL_PROJECTION );
        glLoadIdentity();
        gluOrtho2D( 0, width, 0., height );
        glutMainLoop();

        return 0;
#endif
}

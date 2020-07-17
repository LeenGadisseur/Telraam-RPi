/*	Author: Leen Gadisseur
 *	Description:	backEstimationModule.c 
 *		Dit is het .C bestand behorend tot de "backEstimation" package voor de C-extensie.
 *		Deze module bevat de functies behorend tot de module.		
 *		De belangrijkste functie is de backEstimation.
 *		Het headerbestand: "arrayobject.h" is nodig voor de werking van deze module. Het bestandpad moet dus overeenkomstig aangepast worden.
 *		Dit module bestand wordt gebuild met door 'python3 setup.py build' uittevoeren en het gegenereerde .so bestand in de correcte map te plaatsen.
 *		
 */

#include <stdio.h>
#include <stdint.h>
#include <Python.h>
#include "/home/leen/Documents/AI-ML/labo-ai-student/lib/python3.6/site-packages/numpy/core/include/numpy/arrayobject.h"



/* helloworld(): neemt geen argumenten, print " hello world" uit in de terminal. (test functie) */
static PyObject* helloworld(PyObject* self, PyObject* args)
{
    printf("Hello World\n");
    return Py_None;
}

/* verdubbel(): neemt één argument (python: int). Geeft de verdubbelde waarde terug, verandert niets aan de originele variabele in python. (test functie) */
static PyObject* verdubbel(PyObject* self, PyObject* args)
{
	int a;

 	if( !PyArg_ParseTuple(args, "i", &a)){
		return NULL;
	}

	a = 2*a;
	return Py_BuildValue("i", a);
}

/* example(): neemt één argument ( python: array met type float). Verdubbelt alle ellementen in de array, de array variabele verandert ook in python. (test functie) */
static PyObject* example (PyObject *self, PyObject *args){
	
	PyArrayObject *array; 
	double* waarde1, waarde;

	if( !PyArg_ParseTuple(args, "O!", &PyArray_Type, &array)){
		return NULL;
	}

	if (array->nd != 2 || array->descr->type_num != NPY_DOUBLE) {
		PyErr_SetString(PyExc_ValueError, "array must be two-dimensional and of type float");
		return NULL;

	}

	printf("type in array C: %d \n", array->descr->type_num);
	printf("dimensie: %d \n", array->nd);
	
	waarde1 = (double *)array->data;
	printf("Element :%f \n", *waarde1);
	
	for (int i=0; i<array->dimensions[0]; i++) {
		for (int j=0; j<array->dimensions[1]; j++) {
		   	// onderstaande is in orde -array in python wordt zo ook aangepast.
			waarde = *(double*)(array->data + i*array->strides[0] + j*array->strides[1]);
			*(double*)(array->data + i*array->strides[0] + j*array->strides[1])= (*(double*)(array->data + i*array->strides[0] + j*array->strides[1]))*2;
			printf(" %f", waarde);
				
			//op deze manier wordt de array in python niet aangepast.
			//pixel = *(double*)PyArray_GETPTR2(array, i, j);
			//pixel = 2*pixel;
			//printf("Pixel: %f", pixel);
		    //pixel = *(unsigned int*)PyArray_GETPTR2(array, i, j);
		    //printf("Pixel: %u", pixel);
		}
		
		printf("\n");
	
	}
	return Py_None;
}


/* backEstimationDev(): neemt twee argumenten ( python: twee arrays van type uint8). Verhoogt alle ellementen van de tweede array met 1. Deze array variabele verandert ook in python. (test functie) */
static PyObject* backEstimationDev(PyObject* self,PyObject* args){
	PyArrayObject* frame;
	PyArrayObject* back;
	//unsigned char* pixel;
	unsigned char uno = 1;

	if( !PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &frame, &PyArray_Type, &back)){
		return NULL;
	}

	if (frame->nd != 2 || frame->descr->type_num != NPY_UBYTE) {
		PyErr_SetString(PyExc_ValueError, "array must be two-dimensional and of type float");
		return NULL;

	}

	if (back->nd != 2 || back->descr->type_num != NPY_UBYTE) {
		PyErr_SetString(PyExc_ValueError, "array must be two-dimensional and of type float");
		return NULL;

	}

	printf("type in frame C: %d \n", frame->descr->type_num);
	printf("dimensie van frame: %d \n", frame->nd);
	
	
	for (int i=0; i<frame->dimensions[0]; i++) {
		for (int j=0; j<frame->dimensions[1]; j++) {
		   	// onderstaande is in orde -array in python wordt zo ook aangepast.
			//
			*(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1])= (*(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1])) + uno ;
			//pixel = *(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1]);
			//printf(" %d", pixel);
				
		}
			
		printf("\n");
		
	}
	return Py_None;
}

/* backEstimation(): neemt twee argumenten ( python: twee arrays van type uint8). De eerste array is een frame (gray-waarde), de tweede array is de backgroundestimation 
 * 	Afhankelijk van de waarde in de nieuwe frame, wordt de backgroundestimation array aangepast. Deze array variabele verandert ook in python. 
 */
static PyObject* backEstimation(PyObject* self,PyObject* args){
	PyArrayObject* frame;
	PyArrayObject* back;
	unsigned char uno = 1;

	if( !PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &frame, &PyArray_Type, &back)){
		return NULL;
	}
	//Py_XINCREF(frame);
	//Py_XINCREF(back);	
	
	if (frame->nd != 2 || frame->descr->type_num != NPY_UBYTE) {
		PyErr_SetString(PyExc_ValueError, "\t C: frame array must be two-dimensional and of type unsigned char ( uint8 in python)");
		return NULL;

	}

	if (back->nd != 2 || back->descr->type_num != NPY_UBYTE) {
		PyErr_SetString(PyExc_ValueError, "\t C: back array must be two-dimensional and of type unsigned char ( uint8 in python)");
		return NULL;

	}

	//printf("\t C: type in frame C: %d \n", frame->descr->type_num);
	//printf("\t C: dimensie van frame: %d \n", frame->nd);
	//printf("\t C: dimensie 0 van frame: %ld \n", frame->dimensions[0]);
	//printf("\t C: dimensie 1 van frame: %ld \n", frame->dimensions[1]);
	
	
	for (long i=0; i<frame->dimensions[0]; i++) {
		for (long j=0; j<frame->dimensions[1]; j++) {
		   	if(*(unsigned char*)(frame->data + i*frame->strides[0] + j*frame->strides[1]) >= *(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1]) ){
				*(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1])= (*(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1])) + uno ;
		
			}
			else{
				*(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1])= (*(unsigned char*)(back->data + i*back->strides[0] + j*back->strides[1])) - uno ;
			}	
			
		}
	}
	/*Indien Py_None gereturned wordt, zal dit na X aantal keer te verwijzen/returnen naar gedealloceerd worden waardoor je onderstaande error te zien krijgt: 
		Fatal Python error: deallocating None  
	Dit heeft te maken met de reference count.*/	
	
	//return Py_BuildValue("") werkt;
	//return Py_RETURN_NONE  zou ook moeten werken, (doet het niet?)
	Py_INCREF(Py_None);
	return Py_None;
	
}



static PyMethodDef methods[] = {
	{"backEstimation", backEstimation, METH_VARARGS,"Calculates background estimation. "},
	{"backEstimationDev", backEstimationDev, METH_VARARGS,"Calculates background estimation. "},
	{"example", example, METH_VARARGS,"Example."},
	{ "helloworld", helloworld, METH_NOARGS, "Prints Hello World" },
	{ "verdubbel", verdubbel, METH_VARARGS, "Verdubbelaar" },
	{NULL, NULL,0,NULL}
};


static struct PyModuleDef backEstimationModule = {
	PyModuleDef_HEAD_INIT,
	"backEstimationModule",
	"back estimation Module",
	-1,
	methods
};

PyMODINIT_FUNC PyInit_backEstimation(void){
	import_array();
	return PyModule_Create(&backEstimationModule);
}
/* Types in C en python zijn verschillend: 
 * 	float in python -> double in C
 *	uint8 in python -> unsigned char
 */


/* Types overeenkomend met de typenummers in bovenstaande C-functies.
enum NPY_TYPES {    NPY_BOOL=0,
                    NPY_BYTE, NPY_UBYTE,
                    NPY_SHORT, NPY_USHORT,
                    NPY_INT, NPY_UINT,
                    NPY_LONG, NPY_ULONG,
                    NPY_LONGLONG, NPY_ULONGLONG,
                    NPY_FLOAT, NPY_DOUBLE, NPY_LONGDOUBLE,
                    NPY_CFLOAT, NPY_CDOUBLE, NPY_CLONGDOUBLE,
                    NPY_OBJECT=17,
                    NPY_STRING, NPY_UNICODE,
                    NPY_VOID,
                    
                    NPY_DATETIME, NPY_TIMEDELTA, NPY_HALF,

                    NPY_NTYPES,
                    NPY_NOTYPE,
                    NPY_CHAR NPY_ATTR_DEPRECATE("Use NPY_STRING"),
                    NPY_USERDEF=256,

         
                    NPY_NTYPES_ABI_COMPATIBLE=21
};*/


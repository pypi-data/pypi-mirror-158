#pragma once
#include "Common.h"

struct Edge {
    int u, v;
    std::map<std::string, float>* weight;
};

struct GraphEdge {
    PyObject_HEAD
        Edge edge;
    PyObject* node_to_id, * id_to_node;
};

//��Ϊsequence�ķ���
PyObject* GraphEdge_GetItem(GraphEdge* self, Py_ssize_t index);

//���÷���
PyObject* GraphEdge_repr(GraphEdge* self);

PyObject* GraphEdge_new(PyTypeObject* type, PyObject* args, PyObject* kwds);

void* GraphEdge_dealloc(PyObject* obj);

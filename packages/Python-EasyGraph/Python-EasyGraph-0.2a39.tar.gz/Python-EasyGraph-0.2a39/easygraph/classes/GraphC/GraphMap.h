#pragma once
#include "Common.h"

//�ô�����Ҫ����map��ķ�װ�������뷨������һ��enumö�ٳ�Ա���ͣ�Ȼ�����enum���Ͷ�����η���ֵ
enum MapType { Msf = 0, Mif, Mii, MiMsf, MiMiMsf };

struct GraphMapIter {
    PyObject_HEAD
        MapType type;
    int flag = 0;
    msf_it Msf_iter;
    msf_it Msf_end;
    mif_it Mif_iter;
    mif_it Mif_end;
    mii_it Mii_iter;
    mii_it Mii_end;
    mimsf_it MiMsf_iter;
    mimsf_it MiMsf_end;
    mimimsf_it MiMiMsf_iter;
    mimimsf_it MiMiMsf_end;
    PyObject* id_to_node, * node_to_id;
};

PyObject* GraphMapIter_next(GraphMapIter* self);

PyObject* GraphMapIter_iter(GraphMapIter* self);

PyObject* GraphMapIter_new(PyTypeObject* type, PyObject* args, PyObject* kwds);

void* GraphMapIter_dealloc(PyObject* obj);

/*---------------------------------------------------------------------------------------*/

struct GraphMap {
    PyObject_HEAD
        bool flag = 0;
    MapType type;
    void* pointer;
    PyObject* id_to_node, * node_to_id;
};

PyObject* GraphMap_copy(GraphMap* self, PyObject* args, PyObject* kwds);

PyObject* GraphMap_keys(GraphMap* self, PyObject* args, PyObject* kwds);

PyObject* GraphMap_get(GraphMap* self, PyObject* args, PyObject* kwds);

PyObject* GraphMap_values(GraphMap* self);

PyObject* GraphMap_items(GraphMap* self);

//��Ϊmapping�ķ���
PyObject* GraphMap_getitem(GraphMap* self, PyObject* pykey);

Py_ssize_t GraphMap_len(GraphMap* self);

//��Ϊsequence�ķ���
int GraphMap_contains(GraphMap* self, PyObject* args);

//���÷���
PyObject* GraphMap_new(PyTypeObject* type, PyObject* args, PyObject* kwds);

void* GraphMap_dealloc(PyObject* obj);

PyObject* GraphMap_repr(GraphMap* self);

PyObject* GraphMap_iter(GraphMap* self);

PyObject* _GraphMap_getitem(GraphMap* self, PyObject* pykey, PyObject* default_val);
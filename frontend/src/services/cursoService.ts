import api from './api';

export const importarCursosCsv = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/cursos/importar-csv', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

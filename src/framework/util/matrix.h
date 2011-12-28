/*
 * Copyright (c) 2010-2011 OTClient <https://github.com/edubart/otclient>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#ifndef MATRIX_H
#define MATRIX_H

#include <array>
#include <cstring>
#include <initializer_list>
#include <sstream>

template<int N, int M, typename T = float>
class Matrix
{
public:
    Matrix() { setIdentity(); }
    Matrix(const Matrix<N,M,T>& other) = default;
    template<typename U>
    Matrix(const std::initializer_list<U>& values) { *this = values; }
    template<typename U>
    Matrix(const U *values) { *this = values; }

    void setIdentity();
    bool isIdentity() const;
    void fill(T value);

    Matrix<M,N,T> transposed() const;
    typename std::enable_if<N==M>::type transpose() { *this = transposed(); }

    T *data() { return m[0]; }
    const T *data() const { return m[0]; }
    
    T& operator()(int row, int column) { return m[row-1][column-1]; }
    T operator()(int row, int column) const { return m[row-1][column-1]; }

    Matrix<N,M,T>& operator=(const Matrix<N,M,T>& other) = default;
    template<typename U>
    Matrix<N,M,T>& operator=(const std::initializer_list<U>& values);
    template<typename U>
    Matrix<N,M,T>& operator=(const U *values);
    Matrix<N,M,T>& operator+=(const Matrix<N,M,T>& other);
    Matrix<N,M,T>& operator-=(const Matrix<N,M,T>& other);
    Matrix<N,M,T>& operator*=(T factor);
    Matrix<N,M,T>& operator/=(T divisor);
    bool operator==(const Matrix<N,M,T>& other) const;
    bool operator!=(const Matrix<N,M,T>& other) const;

private:
    Matrix(int) {} // construct without initializing identity matrix
    T m[N][M];
};

template<int N, int M, typename T>
void Matrix<N,M,T>::setIdentity() {
    for(int i=0;i<N;++i) {
        for(int j=0;j<M;++j) {
            if(i==j)
                m[i][j] = 1.0f;
            else
                m[i][j] = 0.0f;
        }
    }
}

template<int N, int M, typename T>
bool Matrix<N,M,T>::isIdentity() const {
    for(int i=0;i<N;++i) {
        for(int j=0;j<M;++j) {
            if((i==j && m[i][j] != 1.0f) || (i!=j && m[i][j] != 0.0f))
                return false;
        }
    }
    return true;
}

template<int N, int M, typename T>
void Matrix<N,M,T>::fill(T value) {
    for(int i=0;i<N*M;++i)
        m[0][i] = value;
}

template<int N, int M, typename T>
Matrix<M,N,T> Matrix<N,M,T>::transposed() const {
    Matrix<M,N,T> result(1);
    for(int i=0;i<N;++i)
        for(int j=0;j<M;++j)
            result.m[j][i] = m[i][j];
        return result;
}

template<int N, int M, typename T>
template<typename U>
Matrix<N,M,T>& Matrix<N,M,T>::operator=(const std::initializer_list<U>& values) {
    auto it = values.begin();
    for(int i=0;i<N*M;++i)
        m[0][i] = *(it++);
    return *this;
}

template<int N, int M, typename T>
template<typename U>
Matrix<N,M,T>& Matrix<N,M,T>::operator=(const U *values) {
    for(int i=0;i<N;++i)
        for(int j=0;j<M;++j)
            m[i][j] = values[i*N + j];
        return *this;
}

template<int N, int M, typename T>
Matrix<N,M,T>& Matrix<N,M,T>::operator+=(const Matrix<N,M,T>& other) {
    for(int i=0;i<N*M;++i)
        m[0][i] += other.m[0][i];
    return *this;
}

template<int N, int M, typename T>
Matrix<N,M,T>& Matrix<N,M,T>::operator-=(const Matrix<N,M,T>& other) {
    for(int i=0;i<N*M;++i)
        m[0][i] -= other.m[0][i];
    return *this;
}

template<int N, int M, typename T>
Matrix<N,M,T>& Matrix<N,M,T>::operator*=(T factor) {
    for(int i=0;i<N*M;++i)
        m[0][i] *= factor;
    return *this;
}

template<int N, int M, typename T>
Matrix<N,M,T>& Matrix<N,M,T>::operator/=(T divisor) {
    for(int i=0;i<N*M;++i)
        m[0][i] /= divisor;
    return *this;
}

template<int N, int M, typename T>
bool Matrix<N,M,T>::operator==(const Matrix<N,M,T>& other) const
{
    for(int i=0;i<N*M;++i)
        if(m[0][i] != other.m[0][i])
            return false;
        return true;
}

template<int N, int M, typename T>
bool Matrix<N,M,T>::operator!=(const Matrix<N,M,T>& other) const
{
    for(int i=0;i<N*M;++i)
        if(m[0][i] != other.m[0][i])
            return true;
        return false;
}

template<int N, int M, typename T>
std::ostream& operator<<(std::ostream& out, const Matrix<N,M,T>& mat)
{
    for(int i=0;i<N;++i) {
        for(int j=0;j<M;++j) {
            out << mat(i,j);
            if(j+1 != M)
                out << " ";
        }
        out << "\n";
    }
    return out;
}

template<int N, int M, typename T>
std::istream& operator>>(std::istream& in, Matrix<N,M,T>& mat)
{
    for(int i=0;i<N;++i)
        for(int j=0;j<M;++j)
            in >> mat(i,j);
        return in;
}

typedef Matrix<4,4> Matrix4x4;
typedef Matrix<3,3> Matrix3x3;
typedef Matrix<2,2> Matrix2x2;

typedef Matrix4x4 Matrix4;
typedef Matrix3x3 Matrix3;
typedef Matrix2x2 Matrix2;

#endif
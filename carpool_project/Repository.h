#pragma once
#include "Utils.h"
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

// ===== TEMPLATE CLASS: Repository =====
template <typename T>
class Repository
{
    vector<T>      items;
    map<string,int> idx;

    void reindex()
    {
        idx.clear();
        for (int i = 0; i < (int)items.size(); ++i)
            idx[toLower(items[i].getName())] = i;
    }
public:
    bool add(const T &v)
    {
        string k = toLower(v.getName());
        if (idx.count(k)) return false;
        idx[k] = (int)items.size();
        items.push_back(v);
        return true;
    }

    bool remove(const string &n)
    {
        auto it = idx.find(toLower(n));
        if (it == idx.end()) return false;
        items.erase(items.begin() + it->second);
        reindex();
        return true;
    }

    T *find(const string &n)
    {
        auto it = idx.find(toLower(n));
        return it == idx.end() ? nullptr : &items[it->second];
    }

    const vector<T> &getAll() const { return items; }
    int size()                const { return (int)items.size(); }

    template<typename Cmp>
    void sortBy(Cmp c) { sort(items.begin(), items.end(), c); reindex(); }

    template<typename Pred>
    vector<T> filter(Pred p) const
    {
        vector<T> r;
        auto it = items.begin();
        while ((it = find_if(it, items.end(), p)) != items.end())
            r.push_back(*it++);
        return r;
    }
};

// ===== Template free functions =====

template<typename T>
const T *findByName(const vector<T> &col, const string &name)
{
    auto it = find_if(col.begin(), col.end(),
                      [&](const T &x){ return toLower(x.getName()) == toLower(name); });
    return it != col.end() ? &(*it) : nullptr;
}

template<typename T>
void displayAll(const vector<T> &col, const string &hdr = "")
{
    if (!hdr.empty()) cout << "\n--- " << hdr << " ---\n";
    if (col.empty())  { cout << "(none)\n"; return; }
    int i = 1;
    for (const T &x : col) { cout << "#" << i++ << " "; x.display(); }
}

template<typename T, typename Cmp>
vector<T> sortedCopy(const vector<T> &col, Cmp c)
{
    vector<T> r = col;
    sort(r.begin(), r.end(), c);
    return r;
}

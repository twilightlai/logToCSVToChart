# -*- coding: utf-8 -*-

import csv
import os
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Union


class csvTool():
    def create(self, dirPath):
        # 每個log最多筆數數量
        arrayLength = 1000

        # 最後的credit csv data creditCSVDataArray
        creditCSVDataArray = [""] * arrayLength
        creditCSVFilePath = join(dirPath, "creditlog.csv")

        # 最後的trunover csv data creditCSVDataArray
        trunoverCSVDataArray = [""] * arrayLength
        trunoverCSVFilePath = join(dirPath, "turnoverlog.csv")

        # 取得所有檔案與子目錄名稱
        files = listdir(dirPath)
        dir_list = sorted(files, key=lambda x: os.path.getmtime(os.path.join(dirPath, x)))
        # 迴圈處理所有檔案
        for f in files:
            # 產生檔案的絕對路徑
            fullpath = join(dirPath, f)
            # 判斷 fullpath 是檔案還是目錄
            if isfile(fullpath):
                # 判斷 fullpath 副檔名是.log
                if os.path.splitext(fullpath)[-1] == ".log":
                    # 檔案名稱
                    print(f)
                    csvDataArrayIndex = 0
                    creditCSVDataArrayIndex = 0
                    trunoverCSVDataArrayIndex = 0
                    # 讀取全部檔案
                    for i in range(arrayLength):
                        # 讀取檔案
                        logfile = open(fullpath)
                        creditCSVData = creditCSVDataArray[creditCSVDataArrayIndex]
                        trunoverCSVData = trunoverCSVDataArray[trunoverCSVDataArrayIndex]
                        # 第一行,紀錄檔案名稱
                        if csvDataArrayIndex == 0:
                            creditCSVData = str(creditCSVData) + str(f.replace("gamerd.jdb199.info-", "")) + str(",")
                            trunoverCSVData = str(trunoverCSVData) + str(f.replace("gamerd.jdb199.info-", "")) + str(
                                ",")
                        # 第二行,開始記錄每筆資料
                        else:
                            creditlog = ""
                            trunoverlog = ""
                            rowsDataArrayIndex = 0
                            rows = csv.reader(logfile)
                            for data in rows:
                                if data[0].find("merged_libs_egret5.js:4") != -1 and len(data) == 4:
                                    # 把log第一筆資料寫到csv的第二筆上
                                    # print(str(csvDataArrayIndex) + " = " + str(rowsDataArrayIndex) + " = " + str(data))
                                    if (csvDataArrayIndex - 1) == rowsDataArrayIndex:
                                        creditlog = data[2]
                                        trunoverlog = data[3]
                                        rowsDataArrayIndex += 1
                                        # print(str(csvDataArrayIndex) + " = " + str(rowsDataArrayIndex) + " = " + str(data))
                                        break
                                    else:
                                        # file.log index 加一
                                        rowsDataArrayIndex += 1
                            if creditlog != "":
                                creditCSVData = str(creditCSVData) + str(creditlog) + str(",")
                            else:
                                creditCSVData = str(creditCSVData) + str(",")
                            if trunoverlog != "":
                                trunoverCSVData = str(trunoverCSVData) + str(trunoverlog) + str(",")
                            else:
                                trunoverCSVData = str(trunoverCSVData) + str(",")
                            # print(csvData)
                        # print(csvData + "["+ str(csvDataArrayIndex) +"] = " +  csvData)
                        creditCSVDataArray[creditCSVDataArrayIndex] = creditCSVData
                        trunoverCSVDataArray[trunoverCSVDataArrayIndex] = trunoverCSVData
                        # file.csv index 加一
                        csvDataArrayIndex += 1
                        creditCSVDataArrayIndex += 1
                        trunoverCSVDataArrayIndex += 1
                        logfile.close()
        # 開啟輸出的 CSV 檔案
        f = open(creditCSVFilePath, 'a')
        # 清除資料
        f.truncate()
        # 寫入資料
        for csvData in creditCSVDataArray:
            f.writelines(csvData + "\n")
        f.close()
        # 開啟輸出的 CSV 檔案
        f = open(trunoverCSVFilePath, 'a')
        # 清除資料
        f.truncate()
        # 寫入資料
        for csvData in trunoverCSVDataArray:
            f.writelines(csvData + "\n")
        f.close()

        return [creditCSVFilePath, trunoverCSVFilePath]


class chartTool():
    def draw(self, creditCSVPath, turnoverCSVPath):
        contain_plot = 5
        print('Start...\n')
        # set one photo contains how many plots
        print('credit chart...')
        plot_count = 0
        plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
        data = pd.read_csv(creditCSVPath)
        creditDirName = os.path.basename(os.path.split(creditCSVPath)[0])
        outPath = os.path.join("output", creditDirName, "")
        if os.path.exists(outPath) == 0:
            os.makedirs(outPath)
        for i in data.columns:
            xArray = []
            xArrayIndex = 0
            for j in range(len(data[i].array)):
                xArray.append(float(xArrayIndex * 3) / 60)
                xArrayIndex += 1
            plt.plot(xArray, data[i], label=i)
            # plt.scatter(xArray, data[i], label = i)
            plot_count += 1
            print(str(plot_count) + ":" + str(contain_plot) + str(i))
            # for clear view
            if plot_count % contain_plot == 0:
                plt.xlabel('times(minute)', fontsize=40)
                plt.ylabel('balance', fontsize=40)
                plt.xticks(fontsize=30)
                plt.yticks(fontsize=30)
                plt.grid()
                plt.legend(loc='lower left', bbox_to_anchor=(0, 1))
                print(outPath + str(int(plot_count / contain_plot)) + '_th_plot_credit.png')
                plt.savefig(outPath + str(int(plot_count / contain_plot)) + '_th_plot_credit.png')
                plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
        plt.xlabel('times(minute)', fontsize=40)
        plt.ylabel('balance', fontsize=40)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.grid()
        plt.legend(loc='lower left', bbox_to_anchor=(0, 1))
        print(outPath + str(int(plot_count / contain_plot) + 1) + '_th_plot_credit.png')
        plt.savefig(outPath + str(int(plot_count / contain_plot) + 1) + '_th_plot_credit.png')

        print('turnover chart...')
        plot_count = 0
        plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
        data = pd.read_csv(turnoverCSVPath)
        turnoverDirName = os.path.basename(os.path.split(turnoverCSVPath)[0])
        outPath = os.path.join("output", turnoverDirName, "")
        if os.path.exists(outPath) == 0:
            os.makedirs(outPath)
        for i in data.columns:
            xArray = []
            xArrayIndex = 0
            endIndex = 0
            for j in range(len(data[i].array)):
                if data[i][j] > 0:
                    endIndex = j
                xArray.append(float(xArrayIndex * 3) / 60)
                xArrayIndex += 1
            plt.scatter(xArray[endIndex], data[i][endIndex], s=500,
                        label=i + "_" + str(xArray[endIndex]) + "_" + str(data[i][endIndex]))
            plot_count += 1
            print(str(plot_count) + ":" + str(contain_plot) + str(i))
            # for clear view
            if plot_count % contain_plot == 0:
                plt.xlabel('times(minute)', fontsize=40)
                plt.ylabel('trunover', fontsize=40)
                plt.xticks(fontsize=30)
                plt.yticks(fontsize=30)
                plt.grid()
                plt.legend(loc='lower left', bbox_to_anchor=(0, 1))
                print(outPath + str(int(plot_count / contain_plot)) + '_th_plot_turnover.png')
                plt.savefig(outPath + str(int(plot_count / contain_plot)) + '_th_plot_turnover.png')
                plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')
        plt.xlabel('times(minute)', fontsize=40)
        plt.ylabel('trunover', fontsize=40)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.grid()
        plt.legend(loc='lower left', bbox_to_anchor=(0, 1))
        print(outPath + str(int(plot_count / contain_plot) + 1) + '_th_plot_turnover.png')
        plt.savefig(outPath + str(int(plot_count / contain_plot) + 1) + '_th_plot_turnover.png')

        print('Done!')


# 取得所有檔案與子目錄名稱
inputPath = os.path.join("input")
files = listdir(inputPath)  # type: List[Union[str, unicode]]
# 迴圈處理所有檔案
for f in files:
    fullpath = join(inputPath, f)
    if os.path.isdir(fullpath):
        csvT = csvTool()
        pathArray = csvT.create(fullpath)
        chartT = chartTool()
        chartT.draw(pathArray[0], pathArray[1])

raw_input()

from unittest.mock import patch
from ipm import argparse, record_writer, send
import sys
import re
import all912
import all907
import csv


def test_argparse_gdf():
    testargs = ["ipm.py", "--gdf", "in/gdf"]
    with patch.object(sys, 'argv', testargs):
        args, interface = argparse()
        assert args["filetype"] == "gdf"
        assert args["in_filename"] == "in/gdf.csv"
        assert not args["transfer"]
        assert re.fullmatch(r"out/INK01\.D[0-9]{6}\.T[0-9]{6}\.P001", args["out_filename"])


def test_argparse_pdd():
    testargs = ["ipm.py", "--pdd", "in/pdd"]
    with patch.object(sys, 'argv', testargs):
        args, interface = argparse()
        assert args["filetype"] == "pdd"
        assert args["in_filename"] == "in/pdd.csv"
        assert not args["transfer"]
        assert re.fullmatch(r"out/PDD01\.D[0-9]{6}\.T[0-9]{6}\.P001", args["out_filename"])


def test_writer_gdf():
    infile = open("in/gdf.csv", encoding="utf-8-sig")
    reader = csv.DictReader(infile)
    interface = all912.Interface()
    for row in reader:
        interface.field.start(row["Scenario"], row["Preset"])
        re_IPM = r"(ONUS|DOM|INTR|INTE|FEE )513086(05|07|01|06|08|50|60|70|98|99|95|91) [01620CSMBA7] (PO|AT|IM|MT|UN)[0-9]{10}\*{8}[0-9]{4}\s{3}[0-9]{6}M\s{23}[0-9]{13}(DB|CR)[A-Z]{3}[0-9]{13}(DB|CR)EUR(\w|\s){25}[0-9]{4}(\w|\s){13}[A-Z]{3}00006[0-9]{11}\s{8}EUR[0-9]{13}(DB|CR)[0-9]{9}(DB|CR)[0-9]{13}(DB|CR)[0-9]{9}(DB|CR)[0-9]{22}([1-6CHOT89]|\s)\s([0-9]|\s){2}\sC[0-9]{5}\s{13}[0-9]{13}(DB|CR)EUR[0-9]{102}\s[0-9]{9}[0-9A-Z]{9}[0-9]{6}(\s|\w){100}[0-9]{4}\s{3}([0-9]|\s){18}\s[0-9]{11}[0-9]{6}[0-9A-Z]{8}[0-9]{41}\s{2}(0{12}\s{2}){5}0{12}(\s|[0-9A-Z]){3}[0-9]{6}\s{2}(\s|[0-9]){3}(\s|[0-9A-Z]){3}(\s|[0-9A-Z]){10}[0-9]{15}\s{2}(\s|[0-9]){2}(\s|[0-9A-Z]){15}[0-2](([0-9]{8}[CD][0-9]{6})|\s{15})(ATM|NA |POI|MAN|CT[1-9])"
        assert re.match(re_IPM, record_writer(row, reader.fieldnames, interface.field))


def test_writer_pdd():
    infile = open("in/pdd.csv", encoding="utf-8-sig")
    reader = csv.DictReader(infile)
    interface = all907.Interface()
    for row in reader:
        interface.field.start(row["Scenario"], row["Preset"])
        re_IPM = r"[0-9]{14}\s{10}2[0-9]{8}\s{14}5[0-9]{5}\*{6}[0-9]{4}"
        assert re.match(re_IPM, record_writer(row, reader.fieldnames, interface.field))


def test_send_gdf():
    responses = send("pyt/INK01.D230601.T140100.P001", "UAT", "GDF")
    assert responses["login"] == "230 User logged in."
    assert responses["change_directory"] == "250 CWD command successful."
    assert responses["transfer"] == "226 Transfer complete."


def test_send_pdd():
    responses = send("pyt/PDD01.D230607.T110404.P001", "UAT", "PDD") 
    assert responses["login"] == "230 User logged in."
    assert responses["change_directory"] == "250 CWD command successful."
    assert responses["transfer"] == "226 Transfer complete."
    
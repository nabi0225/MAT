import json
import shutil

import confuse as confuse
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import click
import yaml
import os

app = Flask(__name__)
CORS(app)
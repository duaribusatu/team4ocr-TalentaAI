import streamlit as st
from scripts.auth import azure_ad_auth

email, username, full_name = azure_ad_auth('home', True)

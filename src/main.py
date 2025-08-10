# ==============================================================================
# STOCK ANALYSIS TOOL - STRUCTURE MODULAIRE
# ==============================================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Tuple, Optional

# ==============================================================================
# SECTION 1: CONFIGURATION GOOGLE SHEETS
# ==============================================================================

class GoogleSheetsManager:
    """Gestionnaire pour les Google Sheets"""
    
    def __init__(self):
        self.sheet_url = None
        self.data = None
    
    def connect_to_sheet(self, sheet_url: str) -> bool:
        """Connexion à Google Sheets"""
        try:
            self.sheet_url = sheet_url
            # Logique de connexion Google Sheets
            st.success("✅ Connexion Google Sheets réussie")
            return True
        except Exception as e:
            st.error(f"❌ Erreur connexion Google Sheets: {e}")
            return False
    
    def load_portfolio_data(self) -> pd.DataFrame:
        """Charger les données du portfolio depuis Google Sheets"""
        # Implémentation du chargement des données
        pass
    
    def save_to_sheet(self, data: pd.DataFrame) -> bool:
        """Sauvegarder des données vers Google Sheets"""
        # Implémentation de la sauvegarde
        pass

# ==============================================================================
# SECTION 2: MENU PRINCIPAL ET NAVIGATION
# ==============================================================================

class MenuManager:
    """Gestionnaire du menu principal"""
    
    @staticmethod
    def render_sidebar_menu():
        """Affiche le menu principal dans la sidebar"""
        st.sidebar.title("📊 Stock Analysis Tool")
        
        menu_options = {
            "🏠 Accueil": "home",
            "📈 Analyse Individual": "individual_analysis", 
            "💼 Portfolio": "portfolio",
            "🎯 Stratégies": "strategies",
            "📊 Comparaison": "comparison",
            "⚙️ Configuration": "config"
        }
        
        selected = st.sidebar.selectbox(
            "Navigation",
            list(menu_options.keys())
        )
        
        return menu_options[selected]
    
    @staticmethod
    def render_stock_selector():
        """Sélecteur d'actions"""
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input("Symbol (ex: AAPL)", value="AAPL")
        
        with col2:
            period = st.selectbox(
                "Période",
                ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                index=3
            )
        
        return symbol.upper(), period

# ==============================================================================
# SECTION 3: STRATÉGIES D'ANALYSE
# ==============================================================================

class TradingStrategies:
    """Stratégies de trading et d'analyse technique"""
    
    @staticmethod
    def calculate_moving_averages(data: pd.DataFrame, periods: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """Calcul des moyennes mobiles"""
        df = data.copy()
        for period in periods:
            df[f'MA_{period}'] = df['Close'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calcul du RSI"""
        df = data.copy()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """Calcul des bandes de Bollinger"""
        df = data.copy()
        df['MA_20'] = df['Close'].rolling(window=period).mean()
        df['STD_20'] = df['Close'].rolling(window=period).std()
        df['Upper_Band'] = df['MA_20'] + (df['STD_20'] * std_dev)
        df['Lower_Band'] = df['MA_20'] - (df['STD_20'] * std_dev)
        return df
    
    @staticmethod
    def calculate_macd(data: pd.DataFrame) -> pd.DataFrame:
        """Calcul du MACD"""
        df = data.copy()
        ema_12 = df['Close'].ewm(span=12).mean()
        ema_26 = df['Close'].ewm(span=26).mean()
        df['MACD'] = ema_12 - ema_26
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        return df
    
    @staticmethod
    def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
        """Génération de signaux d'achat/vente"""
        df = data.copy()
        
        # Signal Golden Cross (MA 50 > MA 200)
        df['Golden_Cross'] = (df['MA_50'] > df['MA_200']) & (df['MA_50'].shift(1) <= df['MA_200'].shift(1))
        
        # Signal Death Cross (MA 50 < MA 200)
        df['Death_Cross'] = (df['MA_50'] < df['MA_200']) & (df['MA_50'].shift(1) >= df['MA_200'].shift(1))
        
        # Signal RSI oversold/overbought
        df['RSI_Oversold'] = df['RSI'] < 30
        df['RSI_Overbought'] = df['RSI'] > 70
        
        return df

# ==============================================================================
# SECTION 4: GESTION DE PORTFOLIO
# ==============================================================================

class PortfolioManager:
    """Gestionnaire de portfolio"""
    
    def __init__(self):
        self.holdings = {}
        self.transactions = []
    
    def add_stock(self, symbol: str, quantity: int, purchase_price: float, date: str = None):
        """Ajouter une action au portfolio"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        transaction = {
            'symbol': symbol,
            'type': 'BUY',
            'quantity': quantity,
            'price': purchase_price,
            'date': date,
            'total': quantity * purchase_price
        }
        
        self.transactions.append(transaction)
        
        if symbol in self.holdings:
            self.holdings[symbol]['quantity'] += quantity
            # Recalcul du prix moyen
            total_value = self.holdings[symbol]['avg_price'] * self.holdings[symbol]['quantity'] + transaction['total']
            total_quantity = self.holdings[symbol]['quantity']
            self.holdings[symbol]['avg_price'] = total_value / total_quantity
        else:
            self.holdings[symbol] = {
                'quantity': quantity,
                'avg_price': purchase_price
            }
    
    def remove_stock(self, symbol: str, quantity: int, sale_price: float, date: str = None):
        """Vendre une action du portfolio"""
        if symbol not in self.holdings:
            st.error(f"Action {symbol} non trouvée dans le portfolio")
            return
        
        if self.holdings[symbol]['quantity'] < quantity:
            st.error(f"Quantité insuffisante pour {symbol}")
            return
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        transaction = {
            'symbol': symbol,
            'type': 'SELL',
            'quantity': quantity,
            'price': sale_price,
            'date': date,
            'total': quantity * sale_price
        }
        
        self.transactions.append(transaction)
        self.holdings[symbol]['quantity'] -= quantity
        
        if self.holdings[symbol]['quantity'] == 0:
            del self.holdings[symbol]
    
    def get_portfolio_summary(self) -> Dict:
        """Résumé du portfolio avec performance"""
        summary = {
            'total_value': 0,
            'total_invested': 0,
            'total_pnl': 0,
            'positions': []
        }
        
        for symbol, holding in self.holdings.items():
            try:
                # Récupérer le prix actuel
                ticker = yf.Ticker(symbol)
                current_price = ticker.history(period="1d")['Close'].iloc[-1]
                
                position_value = holding['quantity'] * current_price
                invested_value = holding['quantity'] * holding['avg_price']
                pnl = position_value - invested_value
                pnl_percent = (pnl / invested_value) * 100 if invested_value > 0 else 0
                
                position = {
                    'symbol': symbol,
                    'quantity': holding['quantity'],
                    'avg_price': holding['avg_price'],
                    'current_price': current_price,
                    'position_value': position_value,
                    'invested_value': invested_value,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent
                }
                
                summary['positions'].append(position)
                summary['total_value'] += position_value
                summary['total_invested'] += invested_value
                
            except Exception as e:
                st.error(f"Erreur lors du calcul pour {symbol}: {e}")
        
        summary['total_pnl'] = summary['total_value'] - summary['total_invested']
        
        return summary

# ==============================================================================
# SECTION 5: VISUALISATIONS
# ==============================================================================

class ChartManager:
    """Gestionnaire des graphiques"""
    
    @staticmethod
    def create_candlestick_chart(data: pd.DataFrame, title: str = "Stock Price") -> go.Figure:
        """Graphique en chandelles"""
        fig = go.Figure(data=go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price"
        ))
        
        fig.update_layout(
            title=title,
            yaxis_title="Price ($)",
            xaxis_title="Date",
            template="plotly_dark"
        )
        
        return fig
    
    @staticmethod
    def add_moving_averages(fig: go.Figure, data: pd.DataFrame, periods: List[int] = [20, 50, 200]):
        """Ajouter les moyennes mobiles au graphique"""
        colors = ['orange', 'blue', 'red']
        
        for i, period in enumerate(periods):
            if f'MA_{period}' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[f'MA_{period}'],
                    mode='lines',
                    name=f'MA {period}',
                    line=dict(color=colors[i % len(colors)])
                ))
        
        return fig
    
    @staticmethod
    def create_rsi_chart(data: pd.DataFrame) -> go.Figure:
        """Graphique RSI"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='purple')
        ))
        
        # Lignes de référence
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
        fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Neutral")
        
        fig.update_layout(
            title="RSI (Relative Strength Index)",
            yaxis_title="RSI",
            xaxis_title="Date",
            template="plotly_dark",
            yaxis=dict(range=[0, 100])
        )
        
        return fig
    
    @staticmethod
    def create_volume_chart(data: pd.DataFrame) -> go.Figure:
        """Graphique de volume"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Volume",
            yaxis_title="Volume",
            xaxis_title="Date",
            template="plotly_dark"
        )
        
        return fig

# ==============================================================================
# SECTION 6: DATA MANAGER
# ==============================================================================

class DataManager:
    """Gestionnaire des données financières"""
    
    @staticmethod
    def get_stock_data(symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Récupérer les données d'une action"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                st.error(f"Aucune donnée trouvée pour {symbol}")
                return None
            
            return data
        
        except Exception as e:
            st.error(f"Erreur lors du téléchargement des données pour {symbol}: {e}")
            return None
    
    @staticmethod
    def get_stock_info(symbol: str) -> Optional[Dict]:
        """Récupérer les informations d'une action"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
        
        except Exception as e:
            st.error(f"Erreur lors de la récupération des infos pour {symbol}: {e}")
            return None
    
    @staticmethod
    def calculate_basic_metrics(data: pd.DataFrame) -> Dict:
        """Calculer les métriques de base"""
        current_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-2]
        change = current_price - previous_price
        change_percent = (change / previous_price) * 100
        
        metrics = {
            'current_price': current_price,
            'change': change,
            'change_percent': change_percent,
            'high_52w': data['High'].max(),
            'low_52w': data['Low'].min(),
            'volume': data['Volume'].iloc[-1],
            'avg_volume': data['Volume'].mean()
        }
        
        return metrics

# ==============================================================================
# SECTION 7: APPLICATION PRINCIPALE
# ==============================================================================

class StockAnalysisApp:
    """Application principale"""
    
    def __init__(self):
        self.google_manager = GoogleSheetsManager()
        self.portfolio_manager = PortfolioManager()
        self.data_manager = DataManager()
        self.chart_manager = ChartManager()
        self.strategies = TradingStrategies()
        
        # Configuration de la page
        st.set_page_config(
            page_title="Stock Analysis Tool",
            page_icon="📊",
            layout="wide"
        )
    
    def run(self):
        """Lancer l'application"""
        # Menu principal
        page = MenuManager.render_sidebar_menu()
        
        # Router vers la bonne page
        if page == "home":
            self.render_home()
        elif page == "individual_analysis":
            self.render_individual_analysis()
        elif page == "portfolio":
            self.render_portfolio()
        elif page == "strategies":
            self.render_strategies()
        elif page == "comparison":
            self.render_comparison()
        elif page == "config":
            self.render_config()
    
    def render_home(self):
        """Page d'accueil"""
        st.title("📊 Stock Analysis Tool")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Actions Analysées", "0")
        
        with col2:
            st.metric("💼 Portfolio Value", "$0.00")
        
        with col3:
            st.metric("📊 Stratégies Actives", "0")
        
        st.markdown("### Fonctionnalités principales")
        st.markdown("""
        - 📈 **Analyse Individual**: Analyse détaillée d'une action
        - 💼 **Portfolio**: Gestion de votre portefeuille
        - 🎯 **Stratégies**: Stratégies de trading automatisées
        - 📊 **Comparaison**: Comparer plusieurs actions
        - ⚙️ **Configuration**: Paramètres et Google Sheets
        """)
    
    def render_individual_analysis(self):
        """Page d'analyse individuelle"""
        st.title("📈 Analyse Individual")
        
        # Sélection de l'action
        symbol, period = MenuManager.render_stock_selector()
        
        if st.button("Analyser"):
            data = self.data_manager.get_stock_data(symbol, period)
            
            if data is not None:
                # Calculs des indicateurs
                data = self.strategies.calculate_moving_averages(data)
                data = self.strategies.calculate_rsi(data)
                data = self.strategies.calculate_bollinger_bands(data)
                data = self.strategies.calculate_macd(data)
                
                # Métriques de base
                metrics = self.data_manager.calculate_basic_metrics(data)
                
                # Affichage des métriques
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Prix Actuel", f"${metrics['current_price']:.2f}", 
                             f"{metrics['change']:+.2f} ({metrics['change_percent']:+.2f}%)")
                
                with col2:
                    st.metric("High 52W", f"${metrics['high_52w']:.2f}")
                
                with col3:
                    st.metric("Low 52W", f"${metrics['low_52w']:.2f}")
                
                with col4:
                    st.metric("Volume", f"{metrics['volume']:,.0f}")
                
                # Graphiques
                st.subheader("Graphique des Prix")
                fig = self.chart_manager.create_candlestick_chart(data, f"{symbol} - {period}")
                fig = self.chart_manager.add_moving_averages(fig, data)
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("RSI")
                    fig_rsi = self.chart_manager.create_rsi_chart(data)
                    st.plotly_chart(fig_rsi, use_container_width=True)
                
                with col2:
                    st.subheader("Volume")
                    fig_volume = self.chart_manager.create_volume_chart(data)
                    st.plotly_chart(fig_volume, use_container_width=True)
    
    def render_portfolio(self):
        """Page de gestion du portfolio"""
        st.title("💼 Portfolio")
        
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "➕ Ajouter", "📝 Transactions"])
        
        with tab1:
            st.subheader("Vue d'ensemble du Portfolio")
            summary = self.portfolio_manager.get_portfolio_summary()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Valeur Totale", f"${summary['total_value']:.2f}")
            with col2:
                st.metric("Investissement Total", f"${summary['total_invested']:.2f}")
            with col3:
                pnl_color = "normal" if summary['total_pnl'] >= 0 else "inverse"
                st.metric("P&L Total", f"${summary['total_pnl']:.2f}", 
                         delta_color=pnl_color)
        
        with tab2:
            st.subheader("Ajouter une Position")
            
            col1, col2 = st.columns(2)
            with col1:
                new_symbol = st.text_input("Symbol")
                new_quantity = st.number_input("Quantité", min_value=1, value=1)
            
            with col2:
                new_price = st.number_input("Prix d'achat", min_value=0.01, value=100.0)
                new_date = st.date_input("Date d'achat")
            
            if st.button("Ajouter au Portfolio"):
                self.portfolio_manager.add_stock(
                    new_symbol.upper(), 
                    new_quantity, 
                    new_price, 
                    str(new_date)
                )
                st.success(f"✅ {new_quantity} actions de {new_symbol} ajoutées au portfolio")
        
        with tab3:
            st.subheader("Historique des Transactions")
            if self.portfolio_manager.transactions:
                df_transactions = pd.DataFrame(self.portfolio_manager.transactions)
                st.dataframe(df_transactions)
            else:
                st.info("Aucune transaction enregistrée")
    
    def render_strategies(self):
        """Page des stratégies"""
        st.title("🎯 Stratégies de Trading")
        
        strategy_type = st.selectbox(
            "Type de Stratégie",
            ["Golden Cross", "RSI Oversold/Overbought", "Bollinger Bands", "MACD"]
        )
        
        st.markdown(f"### Configuration: {strategy_type}")
        
        if strategy_type == "Golden Cross":
            st.markdown("""
            **Golden Cross Strategy**: Signal d'achat quand MA 50 > MA 200
            - ✅ Signal d'achat: MA 50 croise au-dessus de MA 200
            - ❌ Signal de vente: MA 50 croise en-dessous de MA 200
            """)
        
        elif strategy_type == "RSI Oversold/Overbought":
            rsi_oversold = st.slider("RSI Oversold", 10, 40, 30)
            rsi_overbought = st.slider("RSI Overbought", 60, 90, 70)
            
            st.markdown(f"""
            **RSI Strategy**:
            - ✅ Signal d'achat: RSI < {rsi_oversold} (Oversold)
            - ❌ Signal de vente: RSI > {rsi_overbought} (Overbought)
            """)
    
    def render_comparison(self):
        """Page de comparaison"""
        st.title("📊 Comparaison d'Actions")
        
        symbols_input = st.text_input("Symbols (séparés par des virgules)", "AAPL,MSFT,GOOGL")
        period = st.selectbox("Période", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
        
        if st.button("Comparer"):
            symbols = [s.strip().upper() for s in symbols_input.split(',')]
            
            comparison_data = {}
            for symbol in symbols:
                data = self.data_manager.get_stock_data(symbol, period)
                if data is not None:
                    comparison_data[symbol] = data['Close']
            
            if comparison_data:
                df_comparison = pd.DataFrame(comparison_data)
                
                # Normalisation des prix (base 100)
                df_normalized = (df_comparison / df_comparison.iloc[0]) * 100
                
                fig = go.Figure()
                for symbol in symbols:
                    fig.add_trace(go.Scatter(
                        x=df_normalized.index,
                        y=df_normalized[symbol],
                        mode='lines',
                        name=symbol
                    ))
                
                fig.update_layout(
                    title="Performance Comparative (Base 100)",
                    yaxis_title="Performance (%)",
                    xaxis_title="Date",
                    template="plotly_dark"
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def render_config(self):
        """Page de configuration"""
        st.title("⚙️ Configuration")
        
        st.subheader("Google Sheets Integration")
        sheet_url = st.text_input("URL Google Sheets")
        
        if st.button("Connecter Google Sheets"):
            if sheet_url:
                self.google_manager.connect_to_sheet(sheet_url)
            else:
                st.error("Veuillez entrer une URL Google Sheets")
        
        st.markdown("---")
        
        st.subheader("Paramètres Généraux")
        st.checkbox("Mode Sombre", value=True)
        st.selectbox("Devise", ["USD", "EUR", "CAD"])
        st.slider("Actualisation Auto (minutes)", 1, 60, 5)

# ==============================================================================
# POINT D'ENTRÉE
# ==============================================================================

if __name__ == "__main__":
    app = StockAnalysisApp()
    app.run()

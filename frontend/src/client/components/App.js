import React, {Component} from 'react';
import {StaticMap} from 'react-map-gl';
import {DeckGL} from '@deck.gl/react';
import {IconLayer, PathLayer, PolygonLayer, ScatterplotLayer} from '@deck.gl/layers';
import 'antd/dist/antd.less';
import {Button, Checkbox, Radio} from 'antd';
import './App.css';
import jsonp from "../util/jsonp";

const MAPBOX_TOKEN = 'pk.eyJ1IjoiYXJuZTdtb3JnZW4iLCJhIjoiY2o4NGs5ZGZiMDFtaDJ3dWRiMjFnbjNneSJ9.jIMQ2BA0yPSIBeDakaTKug';


let stateCounter = 0;

let paths = [];

export default class App extends Component {
    constructor() {
        super();

        let lonlatZoom = this._getInitCenterLonlatZoom();

        this.state = {
            viewState: {
                longitude: lonlatZoom[0],
                latitude: lonlatZoom[1],
                zoom: lonlatZoom[2],
                maxZoom: 30,
                maxPitch: 60,
                bearing: 0,
                pitch: 0,
            },
            mapStyleId: 'dark',
            mapStyle: 'mapbox://styles/mapbox/dark-v10',
            count: 0,
        };

        jsonp('http://localhost:5000/direction?start=Heidenfeldstr&end=Hermannplatz&mode=driving', (data) => {
            paths = [{line:data.overview_polyline.map(([lat, lon]) => [lon, lat])}];
            console.log(paths);
        });
    }

    _getInitCenterLonlatZoom() {
        let defaultLonlatZoom = [13.406041, 52.519917, 11.7];  // Berlin
        let url = new URL(window.location.href);
        let lon = parseFloat(url.searchParams.get('lon'));
        let lat = parseFloat(url.searchParams.get('lat'));
        return (isNaN(lat) || isNaN(lon)) ? defaultLonlatZoom : [lon, lat, 15];
    }

    _updateState() {
        this.setState({counter: stateCounter++});
    }


    _onViewStateChange({viewState, interactionState, oldViewState}) {
        this.setState({viewState});
    }

    _onMapClick(event) {
        if (event.layer !== null) return; // only consider fallback clicks
        this.setState({
            doFollow: false,
            viewState: {
                ...this.state.viewState,
                transitionDuration: 400,
                zoom: 15,
                bearing: 0,
                pitch: 0,
            }
        });
    }

    _onMapStyleChange(event) {
        let styleId = event.target.value;
        const styleMap = new Map([
            ['light', 'mapbox://styles/mapbox/light-v10'],
            ['dark', 'mapbox://styles/mapbox/dark-v10'],
        ]);

        this.setState({
            mapStyleId: styleId,
            mapStyle: styleMap.get(styleId),
        });
    }

    render() {
        let layers = [];

        layers.push(new PathLayer({
            id: 'segments',
            data: paths,
            opacity: 0.8,
            getPath: d => d.line,
            getColor: d => [255, 0, 0, 255],
            getWidth: 2.5,
            widthMinPixels: 4,
            pickable: true,
            onClick: (event) => console.log(event),
        }));

        return (
            <div id="main">
                <div style={{flexGrow: 1, backgroundColor: '#eee', position: 'relative'}}>
                    <DeckGL
                        ref={(ref) => this.deckInstance = ref}
                        pickingRadius={20}
                        layers={layers}
                        viewState={this.state.viewState}
                        controller={{touchRotate: this.state.viewState.pitch !== 0}}
                        onViewStateChange={this._onViewStateChange.bind(this)}
                        onClick={this._onMapClick.bind(this)}
                    >
                        <StaticMap
                            mapboxApiAccessToken={MAPBOX_TOKEN}
                            mapStyle={this.state.mapStyle}/>
                    </DeckGL>
                </div>
                <div id="control-panel">
                    <span id="control-panel-content">
                        <span>
                            <Radio.Group value={this.state.mapStyleId} onChange={this._onMapStyleChange.bind(this)}>
                                <Radio.Button value="light">light</Radio.Button>
                                <Radio.Button value="dark">dark</Radio.Button>
                            </Radio.Group>
                        </span>
                    </span>
                </div>
            </div>
        );
    }
}

import React, {Component} from 'react';
import {StaticMap} from 'react-map-gl';
import {DeckGL} from '@deck.gl/react';
import {IconLayer, PathLayer, PolygonLayer, ScatterplotLayer} from '@deck.gl/layers';
import 'antd/dist/antd.less';
import {Button, Checkbox, Radio} from 'antd';
import './App.css';
import jsonp from "./jsonp.js";

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
            layers: [],
        };

        jsonp('http://localhost:5000/route?start=Heidenfeldstr&end=Hermannplatz&mode=driving', (data) => {
          let paths = []
          for(let step of data.steps){
            //console.log(step)
            let line = step.polyline.map(([lat, lon]) => [lon, lat])
            let color = this._getColorForMode(step.travel_mode)
            //console.log(line,color)
            paths.push({
              line: line,
              color: color,
            })
          }

            
            
            let paths_one = [{line:data.overview_polyline.map(([lat, lon]) => [lon, lat])}];
            //console.log(paths_one);
            console.log(paths)
            for(let path of paths){
              console.log("pushing new layer")
              //console.log(path)
              this.state.layers.push(new PathLayer({
                id: 'segments'+Math.random(),
                data: path,
                opacity: 0.8,
                getPath: d => d.line,
                getColor: d => d.color,
                getWidth: 2.5,
                widthMinPixels: 4,
                pickable: true,
                onClick: (info) => {this.setState({
                  hoveredObject: info.object,
                  pointerX: info.x,
                  pointerY: info.y
                  });
                  console.log("line clicked")
                  console.log(info)
                  this._renderTooltip(info)
                  }
              }))
            }
        });

        //console.log("in render", paths)
        
    }

    _getColorForMode(mode){
      switch (mode) {
        case "TRANSIT":
          return "#ff0000"
        case "BIKING":
          return "#00ff00"
        case "WALKING":
          return "#ffff00"
        default:
          break;
      }
      
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
        console.log(event)
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
        this._renderTooltip()
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

    _renderTooltip(info) {
      console.log("in renderTooltip")
      const hoveredObject = info.object;
      console.log(hoveredObject, info.x, info.y)
      console.log(info && (
        <div style={{position: 'absolute', zIndex: 1, pointerEvents: 'none', left: info.x, top: info.y}}>
          { "hoveredObject.message" }
        </div>
      ))
      return info && (
        <div style={{position: 'absolute', zIndex: 1, pointerEvents: 'none', left: info.x, top: info.y}}>
          { "hoveredObject.message" }
        </div>
      );
    }


    render() {

        
        console.log(this.state.layers)
        return (
            <div id="main">
                <div style={{flexGrow: 1, backgroundColor: '#eee', position: 'relative'}}>
                    <DeckGL
                        ref={(ref) => this.deckInstance = ref}
                        pickingRadius={20}
                        layers={this.state.layers}
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

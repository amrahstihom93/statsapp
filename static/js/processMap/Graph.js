/**
 * $Id: Graph.js,v 1.14 2013/02/16 10:19:54 gaudenz Exp $
 * Copyright (c) 2006-2012, JGraph Ltd
 */
/**
 * Constructs a new graph instance. Note that the constructor does not take a
 * container because the graph instance is needed for creating the UI, which
 * in turn will create the container for the graph. Hence, the container is
 * assigned later in EditorUi.
 */
Graph = function(container, model, renderHint, stylesheet)
{
	mxGraph.call(this, container, model, renderHint, stylesheet);
	
	this.setConnectable(true);
	this.setDropEnabled(true);
	this.setPanning(true);
	this.setTooltips(!mxClient.IS_TOUCH);
	this.setAllowLoops(true);
	this.allowAutoPanning = true;
	this.resetEdgesOnConnect = false;
	this.constrainChildren = false;
	
	// Enables cloning of connection sources
	this.connectionHandler.setCreateTarget(true);
	
	// Disables built-in connection starts
	this.connectionHandler.isValidSource = function()
	{
		return mxConnectionHandler.prototype.isValidSource.apply(this, arguments) && urlParams['connect'] != '2';
	};

	// Sets the style to be used when an elbow edge is double clicked
	this.alternateEdgeStyle = 'vertical';

	if (stylesheet == null)
	{
		this.loadStylesheet();
	}
	
	// Creates rubberband selection
    var rubberband = new mxRubberband(this);
    
    this.getRubberband = function()
    {
    	return rubberband;
    };
    
    // Shows hand cursor while panning
	this.panningHandler.addListener(mxEvent.PAN_START, mxUtils.bind(this, function()
	{
		this.container.style.cursor = 'pointer';
	}));
			
	this.panningHandler.addListener(mxEvent.PAN_END, mxUtils.bind(this, function()
	{
		this.container.style.cursor = 'default';
	}));

    // Adds support for HTML labels via style. Note: Currently, only the Java
    // backend supports HTML labels but CSS support is limited to the following:
    // http://docs.oracle.com/javase/6/docs/api/index.html?javax/swing/text/html/CSS.html
	this.isHtmlLabel = function(cell)
	{
		var state = this.view.getState(cell);
		var style = (state != null) ? state.style : this.getCellStyle(cell);
		
		return style['html'] == '1' || style['whiteSpace'] == 'wrap';
	};
	
	// HTML entities are displayed as plain text in wrapped plain text labels
	this.cellRenderer.getLabelValue = function(state)
	{
		var result = mxCellRenderer.prototype.getLabelValue.apply(this, arguments);
		
		if (state.style['whiteSpace'] == 'wrap' && state.style['html'] != 1)
		{
			result = mxUtils.htmlEntities(result, false);
		}
		
		return result;
	};
	
	// Unlocks all cells
	this.isCellLocked = function(cell)
	{
		return false;
	};

	// Tap and hold brings up context menu.
	// Tolerance slightly below graph tolerance is better.
	this.connectionHandler.tapAndHoldTolerance = 16;
	
	//  Tap and hold on background starts rubberband on cell starts connecting
	var connectionHandlerTapAndHold = this.connectionHandler.tapAndHold;
	this.connectionHandler.tapAndHold = function(me, state)
	{
		if (state == null)
		{
			if (!this.graph.panningHandler.active)
			{
				rubberband.start(me.getGraphX(), me.getGraphY());
				this.graph.panningHandler.panningTrigger = false;
			}
		}
		else if (tapAndHoldStartsConnection)
		{
			connectionHandlerTapAndHold.apply(this, arguments);	
		}
		else if (this.graph.isCellSelected(state.cell) && this.graph.getSelectionCount() > 1)
		{
			this.graph.removeSelectionCell(state.cell);
		}
	};

	if (touchStyle)
	{
		this.initTouch();
	}
};

// Graph inherits from mxGraph
mxUtils.extend(Graph, mxGraph);

/**
 * Allows to all values in fit.
 */
Graph.prototype.minFitScale = null;

/**
 * Allows to all values in fit.
 */
Graph.prototype.maxFitScale = null;

/**
 * Loads the stylesheet for this graph.
 */
Graph.prototype.loadStylesheet = function()
{
    var node = mxUtils.load(STYLE_PATH + '/default.xml').getDocumentElement();
	var dec = new mxCodec(node.ownerDocument);
	dec.decode(node, this.getStylesheet());
};

/**
 * Inverts the elbow edge style without removing existing styles.
 */
Graph.prototype.flipEdge = function(edge)
{
	if (edge != null)
	{
		var state = this.view.getState(edge);
		var style = (state != null) ? state.style : this.getCellStyle(edge);
		
		if (style != null)
		{
			var elbow = mxUtils.getValue(style, mxConstants.STYLE_ELBOW,
				mxConstants.ELBOW_HORIZONTAL);
			var value = (elbow == mxConstants.ELBOW_HORIZONTAL) ?
				mxConstants.ELBOW_VERTICAL : mxConstants.ELBOW_HORIZONTAL;
			this.setCellStyles(mxConstants.STYLE_ELBOW, value, [edge]);
		}
	}
};

/**
 * Sets the default edge for future connections.
 */
Graph.prototype.setDefaultEdge = function(cell)
{
	if (cell != null && this.getModel().isEdge(cell))
	{
		// Take a snapshot of the cell at the moment of calling
		var proto = this.getModel().cloneCells([cell])[0];
		
		// Delete existing points
		if (proto.geometry != null)
		{
			proto.geometry.points = null;
		}
		
		// Delete entry-/exitXY styles
		var style = proto.getStyle();
		style = mxUtils.setStyle(style, mxConstants.STYLE_ENTRY_X, null);
		style = mxUtils.setStyle(style, mxConstants.STYLE_ENTRY_Y, null);
		style = mxUtils.setStyle(style, mxConstants.STYLE_EXIT_X, null);
		style = mxUtils.setStyle(style, mxConstants.STYLE_EXIT_Y, null);
		proto.setStyle(style);
		
		// Uses edge template for connect preview
		this.connectionHandler.createEdgeState = function(me)
		{
    		return this.graph.view.createState(proto);
	    };

	    // Creates new connections from edge template
	    this.connectionHandler.factoryMethod = function()
	    {
    		return this.graph.cloneCells([proto])[0];
	    };
	}
};

/**
 * Disables folding for non-swimlanes.
 */
Graph.prototype.isCellFoldable = function(cell)
{
	return this.foldingEnabled && this.isSwimlane(cell);
};

/**
 * Disables drill-down for non-swimlanes.
 */
Graph.prototype.isValidRoot = function(cell)
{
	return this.isSwimlane(cell);
};

/**
 * Overrides createGroupCell to set the group style for new groups to 'group'.
 */
Graph.prototype.createGroupCell = function()
{
	var group = mxGraph.prototype.createGroupCell.apply(this, arguments);
	group.setStyle('group');
	
	return group;
};

/**
 * Overrides tooltips to show position and size
 */
Graph.prototype.getTooltipForCell = function(cell)
{
	var tip = '';
	
	if (this.getModel().isVertex(cell))
	{
		var geo = this.getCellGeometry(cell);
		
		var f2 = function(x)
		{
			return Math.round(parseFloat(x) * 100) / 100;
		};
		
		if (geo != null)
		{
			if (tip == null)
			{
				tip = '';
			}
			else if (tip.length > 0)
			{
				tip += '\n';
			}
			
			tip += 'X: ' + f2(geo.x) + '\nY: ' + f2(geo.y) + '\nW: ' + f2(geo.width) + '\nH: ' + f2(geo.height);
		}
	}
	else if (this.getModel().isEdge(cell))
	{
		tip = mxGraph.prototype.getTooltipForCell.apply(this, arguments);
	}
	
	return tip;
};

/**
 * Returns the label for the given cell.
 */
Graph.prototype.convertValueToString = function(cell)
{
	if (cell.value != null && typeof(cell.value) == 'object')
	{
		return cell.value.getAttribute('label');
	}
	
	return mxGraph.prototype.convertValueToString.apply(this, arguments);
};

/**
 * Handles label changes for XML user objects.
 */
Graph.prototype.cellLabelChanged = function(cell, value, autoSize)
{
	if (cell.value != null && typeof(cell.value) == 'object')
	{
		var tmp = cell.value.cloneNode(true);
		tmp.setAttribute('label', value);
		value = tmp;
	}
	
	mxGraph.prototype.cellLabelChanged.apply(this, arguments);
};

/**
 * Sets the link for the given cell.
 */
Graph.prototype.setLinkForCell = function(cell, link)
{
	var value = null;
	
	if (cell.value != null && typeof(cell.value) == 'object')
	{
		value = cell.value.cloneNode(true);
	}
	else
	{
		var doc = mxUtils.createXmlDocument();
		
		value = doc.createElement('UserObject');
		value.setAttribute('label', cell.value);
	}
	
	if (link != null && link.length > 0)
	{
		value.setAttribute('link', link);
	}
	else
	{
		value.removeAttribute('link');
	}
	
	this.model.setValue(cell, value);
};

/**
 * Returns the link for the given cell.
 */
Graph.prototype.getLinkForCell = function(cell)
{
	if (cell.value != null && typeof(cell.value) == 'object')
	{
		return cell.value.getAttribute('link');
	}
	
	return null;
};

/**
 * Customized graph for touch devices.
 */
Graph.prototype.initTouch = function()
{
	// Disables new connections via "hotspot"
	this.connectionHandler.marker.isEnabled = function()
	{
		return this.graph.connectionHandler.first != null;
	};

	// Hides menu when editing starts
	this.addListener(mxEvent.START_EDITING, function(sender, evt)
	{
		this.panningHandler.hideMenu();
	});

	// Context menu for touchstyle
	var showMenu = false;
	var menuCell = null;

	// Checks if native hit detection did not return anything and does custom
	// hit detection for edges to take into account the tolerance
	this.updateMouseEvent = function(me)
	{
		mxGraph.prototype.updateMouseEvent.apply(this, arguments);

		if (me.getState() == null)
		{
			var cell = this.getCellAt(me.graphX, me.graphY);
			
			if (this.getModel().isEdge(cell))
			{
				me.state = this.view.getState(cell);
				
				if (me.state != null && me.state.shape != null)
				{
					this.container.style.cursor = me.state.shape.node.style.cursor;
				}
			}
		}
		
		if (me.getState() == null)
		{
			this.container.style.cursor = 'default';
		}
	};
	
	// Handles popup menu on touch devices (tap selected cell)
	this.fireMouseEvent = function(evtName, me, sender)
	{
		if (evtName == mxEvent.MOUSE_DOWN)
		{
			if (!this.panningHandler.isMenuShowing())
			{
				menuCell = me.getCell();
				showMenu = (menuCell != null) ? this.isCellSelected(menuCell) : this.isSelectionEmpty();
			}
			else
			{
				showMenu = false;
				menuCell = null;
			}
		}
		else if (evtName == mxEvent.MOUSE_UP)
		{
			if (showMenu && !this.isEditing())
			{
				if (!this.panningHandler.isMenuShowing())
				{
					var x = mxEvent.getClientX(me.getEvent());
					var y = mxEvent.getClientY(me.getEvent());
					
					this.panningHandler.popup(x + 16, y, menuCell, me.getEvent());
				}
				
				showMenu = false;
				menuCell = null;
				me.consume();
				
				return;
			}
			
			showMenu = false;
			menuCell = null;
		}

		mxGraph.prototype.fireMouseEvent.apply(this, arguments);

		if (evtName == mxEvent.MOUSE_MOVE && me.isConsumed())
		{
			showMenu = false;
			menuCell = null;
		}
	};
};

/**
 * Implements touch devices.
 */
(function()
{
	// Enables rotation handle
	mxVertexHandler.prototype.rotationEnabled = true;
	
	// Matches label positions of mxGraph 1.x
	mxText.prototype.baseSpacingTop = 5;
	mxText.prototype.baseSpacingBottom = 1;

	// Touch-specific static overrides
	if (touchStyle)
	{
		// Sets constants for touch style
		mxConstants.HANDLE_SIZE = 16;
		mxConstants.LABEL_HANDLE_SIZE = 7;
		
		// Larger tolerance and grid for real touch devices
		if (mxClient.IS_TOUCH)
		{
			mxVertexHandler.prototype.tolerance = 4;
			mxEdgeHandler.prototype.tolerance = 6;
			Graph.prototype.tolerance = 14;
			Graph.prototype.gridSize = 20;
			
			// One finger pans (no rubberband selection) must start regardless of mouse button
			mxPanningHandler.prototype.selectOnPopup = false;
			mxPanningHandler.prototype.useLeftButtonForPanning = true;
			mxPanningHandler.prototype.isPanningTrigger = function(me)
			{
				var evt = me.getEvent();
			 	
			 	return (this.useLeftButtonForPanning && (this.ignoreCell || me.getState() == null)/* &&
			 			mxEvent.isLeftMouseButton(evt)*/) || (mxEvent.isControlDown(evt) &&
			 			mxEvent.isShiftDown(evt)) || (this.usePopupTrigger &&
			 		   	mxEvent.isPopupTrigger(evt));
			};
		}
		
		// Don't clear selection if multiple cells selected
		var graphHandlerMouseDown = mxGraphHandler.prototype.mouseDown;
		mxGraphHandler.prototype.mouseDown = function(sender, me)
		{
			graphHandlerMouseDown.apply(this, arguments);

			if (this.graph.isCellSelected(me.getCell()) && this.graph.getSelectionCount() > 1)
			{
				this.delayedSelection = false;
			}
		};

		// Changes order of panninghandler
		Graph.prototype.createHandlers = function(container)
		{
			this.tooltipHandler = new mxTooltipHandler(this);
			this.tooltipHandler.setEnabled(false);
			// Selection cells first
			this.selectionCellsHandler = new mxSelectionCellsHandler(this);
			this.panningHandler = new mxPanningHandler(this);
			this.panningHandler.panningEnabled = false;
			this.connectionHandler = new mxConnectionHandler(this);
			this.connectionHandler.setEnabled(false);
			this.graphHandler = new mxGraphHandler(this);
		};

		// On connect the target is selected and we clone the cell of the preview edge for insert
		mxConnectionHandler.prototype.selectCells = function(edge, target)
		{
			if (touchStyle && target != null)
			{
				this.graph.setSelectionCell(target);
			}
			else
			{
				this.graph.setSelectionCell(edge);
			}
		};

		// Overrides double click handling to use the tolerance
		// FIXME: Double click on edges in iPad needs focus on textarea
		var graphDblClick = mxGraph.prototype.dblClick;
		Graph.prototype.dblClick = function(evt, cell)
		{
			if (cell == null)
			{
				var pt = mxUtils.convertPoint(this.container,
					mxEvent.getClientX(evt), mxEvent.getClientY(evt));
				cell = this.getCellAt(pt.x, pt.y);
			}

			graphDblClick.call(this, evt, cell);
		};

		// Rounded edge and vertex handles
		var touchHandle = new mxImage(IMAGE_PATH + '/touch-handle.png', 16, 16);
		mxVertexHandler.prototype.handleImage = touchHandle;
		mxEdgeHandler.prototype.handleImage = touchHandle;
		mxOutline.prototype.sizerImage = touchHandle;
		
		// Pre-fetches touch handle
		new Image().src = touchHandle.src;

		// Adds connect icon to selected vertices
		var connectorSrc = IMAGE_PATH + '/touch-connector.png';
		
		var vertexHandlerInit = mxVertexHandler.prototype.init;
		mxVertexHandler.prototype.init = function()
		{
			vertexHandlerInit.apply(this, arguments);

			// Only show connector image on one cell and do not show on containers
			if (showConnectorImg && this.graph.connectionHandler.isEnabled() &&
				this.graph.isCellConnectable(this.state.cell) &&
				!this.graph.isValidRoot(this.state.cell) &&
				this.graph.getSelectionCount() == 1)
			{
				this.connectorImg = mxUtils.createImage(connectorSrc);
				this.connectorImg.style.cursor = 'pointer';
				this.connectorImg.style.width = '29px';
				this.connectorImg.style.height = '29px';
				this.connectorImg.style.position = 'absolute';
				
				if (!mxClient.IS_TOUCH)
				{
					this.connectorImg.setAttribute('title', mxResources.get('connect'));
					mxEvent.redirectMouseEvents(this.connectorImg, this.graph, this.state);
				}

				// Adds 2px tolerance
				this.connectorImg.style.padding = '2px';
				
				// Starts connecting on touch/mouse down
				mxEvent.addGestureListeners(this.connectorImg,
					mxUtils.bind(this, function(evt)
					{
						this.graph.panningHandler.hideMenu();
						var pt = mxUtils.convertPoint(this.graph.container,
								mxEvent.getClientX(evt), mxEvent.getClientY(evt));
						this.graph.connectionHandler.start(this.state, pt.x, pt.y);
						this.graph.isMouseDown = true;
						mxEvent.consume(evt);
					})
				);

				this.graph.container.appendChild(this.connectorImg);
			}

			this.redrawTools();
		};
		
		var vertexHandlerRedraw = mxVertexHandler.prototype.redraw;
		mxVertexHandler.prototype.redraw = function()
		{
			vertexHandlerRedraw.apply(this);
			this.redrawTools();
		};
		
		mxVertexHandler.prototype.redrawTools = function()
		{
			if (this.state != null && this.connectorImg != null)
			{
				// Top right for single-sizer
				if (mxVertexHandler.prototype.singleSizer)
				{
					this.connectorImg.style.left = (this.state.x + this.state.width - this.connectorImg.offsetWidth / 2) + 'px';
					this.connectorImg.style.top = (this.state.y - this.connectorImg.offsetHeight / 2) + 'px';
				}
				else
				{
					this.connectorImg.style.left = (this.state.x + this.state.width + mxConstants.HANDLE_SIZE / 2 + 4/* - 2 padding*/) + 'px';
					this.connectorImg.style.top = (this.state.y + (this.state.height - this.connectorImg.offsetHeight) / 2) + 'px';
				}
			}
		};
		
		var vertexHandlerDestroy = mxVertexHandler.prototype.destroy;
		mxVertexHandler.prototype.destroy = function(sender, me)
		{
			vertexHandlerDestroy.apply(this, arguments);

			if (this.connectorImg != null)
			{
				this.connectorImg.parentNode.removeChild(this.connectorImg);
				this.connectorImg = null;
			}
		};
		
		// Pre-fetches touch connector
		new Image().src = connectorSrc;
	}
	else
	{
		var img = new mxImage(IMAGE_PATH + '/connector.png', 15, 15);
		mxConnectionHandler.prototype.connectImage = img;

		// Pre-fetches img
		new Image().src = img.src;
		
		if (urlParams['connect'] == '2') // not touchStyle
		{
			var img = new mxImage(IMAGE_PATH + '/connector.png', 15, 15);
					
			var vertexHandlerInit = mxVertexHandler.prototype.init;
			mxVertexHandler.prototype.init = function()
			{
				vertexHandlerInit.apply(this, arguments);
	
				// Only show connector image on one cell and do not show on containers
				if (showConnectorImg && this.graph.connectionHandler.isEnabled() &&
					this.graph.isCellConnectable(this.state.cell) &&
					!this.graph.isValidRoot(this.state.cell) &&
					this.graph.getSelectionCount() == 1)
				{
					// Workaround for event redirection via image tag in quirks and IE8
					if (mxClient.IS_IE && !mxClient.IS_SVG)
					{
						this.connectorImg = document.createElement('div');
						this.connectorImg.style.backgroundImage = 'url(' + img.src + ')';
						this.connectorImg.style.backgroundPosition = 'center';
						this.connectorImg.style.backgroundRepeat = 'no-repeat';
						this.connectorImg.style.width = (img.width + 4) + 'px';
						this.connectorImg.style.height = (img.height + 4) + 'px';
						this.connectorImg.style.display = (mxClient.IS_QUIRKS) ? 'inline' : 'inline-block';
					}
					else
					{
						this.connectorImg = mxUtils.createImage(img.src);
						this.connectorImg.style.width = img.width + 'px';
						this.connectorImg.style.height = img.height + 'px';
					}
					
					this.connectorImg.style.cursor = 'pointer';
					this.connectorImg.style.position = 'absolute';
					this.connectorImg.setAttribute('title', mxResources.get('connect'));
					mxEvent.redirectMouseEvents(this.connectorImg, this.graph, this.state);
					
					// Adds 2px tolerance
					this.connectorImg.style.padding = '2px';
					
					// Starts connecting on touch/mouse down
					mxEvent.addListener(this.connectorImg, 'mousedown',
						mxUtils.bind(this, function(evt)
						{
							this.graph.panningHandler.hideMenu();
							var pt = mxUtils.convertPoint(this.graph.container,
									mxEvent.getClientX(evt), mxEvent.getClientY(evt));
							this.graph.connectionHandler.start(this.state, pt.x, pt.y);
							this.graph.isMouseDown = true;
							mxEvent.consume(evt);
						})
					);
	
					this.graph.container.appendChild(this.connectorImg);
				}
	
				this.redrawTools();
			};
			
			var vertexHandlerRedraw = mxVertexHandler.prototype.redraw;
			mxVertexHandler.prototype.redraw = function()
			{
				vertexHandlerRedraw.apply(this);
				this.redrawTools();
			};
			
			mxVertexHandler.prototype.redrawTools = function()
			{
				if (this.state != null && this.connectorImg != null)
				{
					// Top right for single-sizer
					if (mxVertexHandler.prototype.singleSizer)
					{
						this.connectorImg.style.left = (this.state.x + this.state.width - this.connectorImg.offsetWidth / 2) + 'px';
						this.connectorImg.style.top = (this.state.y - this.connectorImg.offsetHeight / 2) + 'px';
					}
					else
					{
						this.connectorImg.style.left = (this.state.x + this.state.width + mxConstants.HANDLE_SIZE / 2 + 2/* - 2 padding*/) + 'px';
						this.connectorImg.style.top = (this.state.y + (this.state.height - this.connectorImg.offsetHeight) / 2) + 'px';
					}
				}
			};
			
			var vertexHandlerDestroy = mxVertexHandler.prototype.destroy;
			mxVertexHandler.prototype.destroy = function(sender, me)
			{
				vertexHandlerDestroy.apply(this, arguments);
	
				if (this.connectorImg != null)
				{
					this.connectorImg.parentNode.removeChild(this.connectorImg);
					this.connectorImg = null;
				}
			};
		}
	}
})();
